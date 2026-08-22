from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sqlite3
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import pandas as pd
import requests
from rapidfuzz import fuzz


# ============================================================
# 사용자 설정
# ============================================================

SERPAPI_KEY = "b8bd2d6f57a74e01f94637cf97edb023a42731a2decd57cf608c2784d9f134c9"

BASE_DIR = Path("/Users/hyowonkim/Downloads")

INPUT_FILE = BASE_DIR / "rq2analticsample_with_kci_metadata_unique.csv"
OUTPUT_FILE = BASE_DIR / "google_scholar_test10_results.csv"
CACHE_DB_FILE = BASE_DIR / "google_scholar_test10_cache.sqlite"
ERROR_LOG_FILE = BASE_DIR / "google_scholar_test10_errors.log"

RESULTS_PER_PAGE = 20
MAX_QUERIES_PER_PAPER = 3
MAX_TITLE_VARIANTS = 2

ENABLE_AUTHOR_REFINED_SEARCH = True
ENABLE_SELECTIVE_SECOND_PAGE = True

# 높은 점수면 바로 확정하고 추가 검색하지 않음
HIGH_CONFIDENCE_TITLE_SCORE = 92.0
HIGH_CONFIDENCE_WEIGHTED_SCORE = 91.0

# 이 기준 이상이면 매칭으로 확정
ACCEPT_TITLE_SCORE = 88.0
ACCEPT_WEIGHTED_SCORE = 87.0

# 이 기준 이상이지만 확정 기준 미달이면 review
REVIEW_TITLE_SCORE = 75.0
REVIEW_WEIGHTED_SCORE = 76.0

# 두 번째 페이지는 첫 페이지 후보가 애매할 때만 사용
SECOND_PAGE_MIN_SCORE = 68.0
SECOND_PAGE_MAX_SCORE = 89.0

REQUEST_TIMEOUT_SECONDS = 60
MAX_RETRIES = 5
BASE_RETRY_SECONDS = 3.0
REQUEST_SLEEP_SECONDS = 0.05


# ============================================================
# 공통 유틸리티
# ============================================================

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass

    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null", "<na>", "n/a"}:
        return ""
    return text


def safe_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    try:
        return int(float(value))
    except (TypeError, ValueError, OverflowError):
        return None


def normalize_title(value: Any) -> str:
    text = unicodedata.normalize("NFKC", clean_text(value)).lower()
    text = re.sub(r"^\s*\[(?:pdf|html|book|citation)\]\s*", "", text)
    text = re.sub(r"[^0-9a-z가-힣一-龥ぁ-んァ-ン]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_author(value: Any) -> str:
    text = unicodedata.normalize("NFKC", clean_text(value)).lower()
    text = re.sub(r"\bet\s+al\.?", " ", text)
    text = re.sub(r"\s+외\s*\d*\s*인?", " ", text)
    text = re.sub(r"[^0-9a-z가-힣一-龥ぁ-んァ-ン]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def split_authors(value: Any) -> list[str]:
    text = clean_text(value)
    if not text:
        return []

    parts = re.split(
        r"\s*(?:;|\||/|\band\b|&|ㆍ|·)\s*",
        text,
        flags=re.IGNORECASE,
    )
    authors = [normalize_author(x) for x in parts]
    authors = [x for x in authors if x]

    if len(authors) <= 1 and "," in text:
        comma_authors = [normalize_author(x) for x in text.split(",")]
        comma_authors = [x for x in comma_authors if x]
        if len(comma_authors) > 1:
            authors = comma_authors

    return list(dict.fromkeys(authors))


def author_search_token(value: Any) -> str:
    authors = split_authors(value)
    if not authors:
        return ""

    first = authors[0]
    tokens = first.split()
    if not tokens:
        return ""

    if re.search(r"[a-z]", first):
        token = tokens[-1]
    else:
        token = "".join(tokens)

    return re.sub(r"[^0-9a-z가-힣一-龥ぁ-んァ-ン]", "", token)


def extract_year(value: Any) -> Optional[int]:
    text = clean_text(value)
    matches = re.findall(r"(?<!\d)(18\d{2}|19\d{2}|20\d{2}|21\d{2})(?!\d)", text)
    return int(matches[-1]) if matches else None


def get_domain(url: Any) -> str:
    text = clean_text(url)
    if not text:
        return ""
    try:
        domain = urlparse(text).netloc.lower()
    except ValueError:
        return ""
    return domain[4:] if domain.startswith("www.") else domain


def looks_like_pdf(url: Any) -> bool:
    text = clean_text(url).lower()
    return bool(text) and (
        urlparse(text).path.lower().endswith(".pdf")
        or ".pdf?" in text
        or "/pdf/" in text
    )


def looks_like_direct_file(url: Any) -> bool:
    text = clean_text(url).lower()
    if not text:
        return False
    path = urlparse(text).path.lower()
    return path.endswith((".pdf", ".doc", ".docx", ".rtf", ".ps", ".ps.gz", ".epub"))


def log_error(message: str) -> None:
    ERROR_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now_utc_iso()}] {message}\n")


# ============================================================
# SQLite 검색 캐시
# ============================================================

def open_cache_db() -> sqlite3.Connection:
    conn = sqlite3.connect(CACHE_DB_FILE, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS query_cache (
            cache_key TEXT PRIMARY KEY,
            params_json TEXT NOT NULL,
            response_json TEXT NOT NULL,
            saved_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def make_cache_key(params: dict[str, Any]) -> str:
    public_params = {k: params[k] for k in sorted(params) if k != "api_key"}
    raw = json.dumps(public_params, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def read_cache(conn: sqlite3.Connection, cache_key: str) -> Optional[dict[str, Any]]:
    row = conn.execute(
        "SELECT response_json FROM query_cache WHERE cache_key = ?",
        (cache_key,),
    ).fetchone()
    return json.loads(row[0]) if row else None


def save_cache(
    conn: sqlite3.Connection,
    cache_key: str,
    params: dict[str, Any],
    response: dict[str, Any],
) -> None:
    public_params = {k: v for k, v in params.items() if k != "api_key"}
    conn.execute(
        """
        INSERT OR REPLACE INTO query_cache
        (cache_key, params_json, response_json, saved_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            cache_key,
            json.dumps(public_params, ensure_ascii=False, sort_keys=True),
            json.dumps(response, ensure_ascii=False),
            now_utc_iso(),
        ),
    )
    conn.commit()


# ============================================================
# SerpAPI 응답 축약 및 요청
# ============================================================

def compact_result(result: dict[str, Any]) -> dict[str, Any]:
    publication_info = result.get("publication_info") or {}
    inline_links = result.get("inline_links") or {}
    cited_by = inline_links.get("cited_by") or {}
    versions = inline_links.get("versions") or {}

    authors = []
    for author in publication_info.get("authors") or []:
        if isinstance(author, dict):
            authors.append(
                {
                    "name": clean_text(author.get("name")),
                    "author_id": clean_text(author.get("author_id")),
                }
            )

    resources = []
    for resource in result.get("resources") or []:
        if isinstance(resource, dict):
            resources.append(
                {
                    "title": clean_text(resource.get("title")),
                    "file_format": clean_text(resource.get("file_format")),
                    "link": clean_text(resource.get("link")),
                }
            )

    return {
        "position": result.get("position"),
        "title": clean_text(result.get("title")),
        "result_id": clean_text(result.get("result_id")),
        "type": clean_text(result.get("type")),
        "link": clean_text(result.get("link")),
        "snippet": clean_text(result.get("snippet")),
        "publication_summary": clean_text(publication_info.get("summary")),
        "authors": authors,
        "resources": resources,
        "html_version": clean_text(inline_links.get("html_version")),
        "citation_count": cited_by.get("total"),
        "cites_id": clean_text(cited_by.get("cites_id")),
        "cited_by_url": clean_text(cited_by.get("link")),
        "versions_count": versions.get("total"),
        "cluster_id": clean_text(versions.get("cluster_id")),
        "versions_url": clean_text(versions.get("link")),
        "related_pages_url": clean_text(inline_links.get("related_pages_link")),
        "cached_page_url": clean_text(inline_links.get("cached_page_link")),
    }


def compact_response(payload: dict[str, Any]) -> dict[str, Any]:
    metadata = payload.get("search_metadata") or {}
    info = payload.get("search_information") or {}

    return {
        "search_metadata": {
            "id": clean_text(metadata.get("id")),
            "status": clean_text(metadata.get("status")),
            "google_scholar_url": clean_text(metadata.get("google_scholar_url")),
        },
        "search_information": {
            "organic_results_state": clean_text(info.get("organic_results_state")),
            "total_results": info.get("total_results"),
            "query_displayed": clean_text(info.get("query_displayed")),
        },
        "organic_results": [
            compact_result(x)
            for x in (payload.get("organic_results") or [])
            if isinstance(x, dict)
        ],
        "api_error": clean_text(payload.get("error")),
    }


def serpapi_search(
    conn: sqlite3.Connection,
    session: requests.Session,
    query: str,
    start: int = 0,
) -> tuple[dict[str, Any], bool]:
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "num": RESULTS_PER_PAGE,
        "start": start,
        "as_vis": 1,
        "as_sdt": 0,
        "filter": 1,
        "output": "json",
    }

    cache_key = make_cache_key(params)
    cached = read_cache(conn, cache_key)
    if cached is not None:
        return cached, False

    last_error = ""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(
                "https://serpapi.com/search.json",
                params=params,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else BASE_RETRY_SECONDS * 2 ** (attempt - 1)
                time.sleep(wait)
                continue

            response.raise_for_status()
            compact = compact_response(response.json())
            save_cache(conn, cache_key, params, compact)
            time.sleep(REQUEST_SLEEP_SECONDS)
            return compact, True

        except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            log_error(f"query={query!r}, start={start}, attempt={attempt}, error={last_error}")
            if attempt < MAX_RETRIES:
                time.sleep(BASE_RETRY_SECONDS * 2 ** (attempt - 1))

    failed = {
        "search_metadata": {"id": "", "status": "Error", "google_scholar_url": ""},
        "search_information": {
            "organic_results_state": "",
            "total_results": None,
            "query_displayed": query,
        },
        "organic_results": [],
        "api_error": last_error,
    }
    save_cache(conn, cache_key, params, failed)
    return failed, True


# ============================================================
# 검색어 후보
# ============================================================

def first_nonempty(row: pd.Series, columns: list[str]) -> str:
    for col in columns:
        value = clean_text(row.get(col))
        if value:
            return value
    return ""


def build_title_variants(row: pd.Series) -> list[dict[str, str]]:
    candidates = [
        {
            "title": clean_text(row.get("kci_title_english")),
            "author": first_nonempty(
                row,
                ["kci_authors_english", "kci_authors_korean", "ref_author"],
            ),
            "source": "kci_english",
        },
        {
            "title": clean_text(row.get("kci_title_original")),
            "author": first_nonempty(
                row,
                ["kci_authors_korean", "kci_authors_english", "ref_author"],
            ),
            "source": "kci_original",
        },
        {
            "title": clean_text(row.get("ref_title")),
            "author": clean_text(row.get("ref_author")),
            "source": "reference",
        },
    ]

    variants = []
    seen = set()

    for item in candidates:
        norm = normalize_title(item["title"]).replace(" ", "")
        if norm and norm not in seen:
            seen.add(norm)
            variants.append(item)

    return variants[:MAX_TITLE_VARIANTS]


def exact_title_query(title: str) -> str:
    title = re.sub(r"\s+", " ", clean_text(title).replace('"', " ")).strip()
    return f'"{title}"' if title else ""


def author_refined_query(title: str, author: str) -> str:
    base = exact_title_query(title)
    token = author_search_token(author)
    return f"{base} author:{token}" if base and token else base


# ============================================================
# 매칭 점수
# ============================================================

def title_similarity(a: Any, b: Any) -> float:
    left = normalize_title(a)
    right = normalize_title(b)
    if not left or not right:
        return 0.0

    return float(
        max(
            fuzz.ratio(left, right),
            fuzz.token_sort_ratio(left, right),
            fuzz.token_set_ratio(left, right),
            fuzz.ratio(left.replace(" ", ""), right.replace(" ", "")),
        )
    )


def author_similarity(
    input_authors: Any,
    result_authors: list[dict[str, Any]],
    publication_summary: str,
) -> Optional[float]:
    left = split_authors(input_authors)

    right = [
        normalize_author(x.get("name"))
        for x in result_authors
        if isinstance(x, dict) and normalize_author(x.get("name"))
    ]

    if not right and publication_summary:
        right = split_authors(publication_summary.split(" - ", 1)[0])

    if not left or not right:
        return None

    return float(
        max(
            max(
                fuzz.ratio(a, b),
                fuzz.token_sort_ratio(a, b),
                fuzz.ratio(a.replace(" ", ""), b.replace(" ", "")),
            )
            for a in left[:5]
            for b in right[:5]
        )
    )


def input_year(row: pd.Series) -> Optional[int]:
    for col in ["kci_pub_year", "search_pub_year", "ref_year"]:
        year = extract_year(row.get(col))
        if year is not None:
            return year
    return None


def input_journal(row: pd.Series) -> str:
    return first_nonempty(
        row,
        ["kci_journal_name", "search_journal_name", "ref_publisher_or_journal"],
    )


def score_candidate(
    row: pd.Series,
    variant: dict[str, str],
    candidate: dict[str, Any],
    query: str,
    start: int,
    response: dict[str, Any],
) -> dict[str, Any]:
    t_score = title_similarity(variant["title"], candidate.get("title"))

    a_score = author_similarity(
        variant["author"],
        candidate.get("authors") or [],
        clean_text(candidate.get("publication_summary")),
    )

    expected_year = input_year(row)
    found_year = extract_year(candidate.get("publication_summary"))
    year_match = (
        expected_year == found_year
        if expected_year is not None and found_year is not None
        else None
    )

    journal = normalize_title(input_journal(row))
    summary = normalize_title(candidate.get("publication_summary"))
    j_score = (
        float(max(fuzz.partial_ratio(journal, summary), fuzz.token_set_ratio(journal, summary)))
        if journal and summary
        else None
    )

    parts = [(t_score, 0.72)]
    if a_score is not None:
        parts.append((a_score, 0.15))
    if year_match is not None:
        parts.append((100.0 if year_match else 0.0, 0.09))
    if j_score is not None:
        parts.append((j_score, 0.04))

    weighted = sum(s * w for s, w in parts) / sum(w for _, w in parts)

    position = safe_int(candidate.get("position"))
    global_position = start + position if position is not None else None

    corroboration = 0
    if a_score is not None and a_score >= 70:
        corroboration += 1
    if year_match is True:
        corroboration += 1
    if j_score is not None and j_score >= 70:
        corroboration += 1

    return {
        "candidate": candidate,
        "query": query,
        "query_source": variant["source"],
        "search_start": start,
        "search_page": start // RESULTS_PER_PAGE + 1,
        "result_position": position,
        "global_result_position": global_position,
        "title_score": round(t_score, 4),
        "author_score": round(a_score, 4) if a_score is not None else None,
        "journal_score": round(j_score, 4) if j_score is not None else None,
        "year_match": year_match,
        "candidate_year": found_year,
        "corroboration_count": corroboration,
        "weighted_score": round(weighted, 4),
        "search_metadata": response.get("search_metadata") or {},
        "search_information": response.get("search_information") or {},
    }


def rank_results(
    row: pd.Series,
    variant: dict[str, str],
    query: str,
    start: int,
    response: dict[str, Any],
) -> list[dict[str, Any]]:
    scored = [
        score_candidate(row, variant, candidate, query, start, response)
        for candidate in response.get("organic_results") or []
    ]
    return sorted(
        scored,
        key=lambda x: (
            x["weighted_score"],
            x["title_score"],
            x["corroboration_count"],
            -(x["global_result_position"] if x["global_result_position"] is not None else 9999),
        ),
        reverse=True,
    )


def classify(candidate: Optional[dict[str, Any]]) -> tuple[str, str, bool]:
    if candidate is None:
        return "not_indexed", "none", False

    weighted = candidate["weighted_score"]
    title = candidate["title_score"]
    corroboration = candidate["corroboration_count"]

    if title >= 98 and weighted >= 90:
        return "matched", "high", True

    if (
        title >= HIGH_CONFIDENCE_TITLE_SCORE
        and weighted >= HIGH_CONFIDENCE_WEIGHTED_SCORE
        and corroboration >= 1
    ):
        return "matched", "high", True

    if (
        title >= ACCEPT_TITLE_SCORE
        and weighted >= ACCEPT_WEIGHTED_SCORE
        and (corroboration >= 1 or title >= 96)
    ):
        return "matched", "medium", True

    if title >= REVIEW_TITLE_SCORE or weighted >= REVIEW_WEIGHTED_SCORE:
        return "review", "low", False

    return "not_indexed", "none", False


# ============================================================
# 접근성 변수
# ============================================================

def access_metadata(candidate: dict[str, Any]) -> dict[str, Any]:
    resources = candidate.get("resources") or []

    formats = []
    urls = []
    domains = []
    titles = []

    for resource in resources:
        fmt = clean_text(resource.get("file_format")).upper()
        url = clean_text(resource.get("link"))
        title = clean_text(resource.get("title"))

        if fmt:
            formats.append(fmt)
        if url:
            urls.append(url)
            domain = get_domain(url)
            if domain:
                domains.append(domain)
        if title:
            titles.append(title)

    html_version = clean_text(candidate.get("html_version"))
    if html_version:
        formats.append("HTML")
        urls.append(html_version)
        domain = get_domain(html_version)
        if domain:
            domains.append(domain)

    formats = list(dict.fromkeys(formats))
    urls = list(dict.fromkeys(urls))
    domains = list(dict.fromkeys(domains))
    titles = list(dict.fromkeys(titles))

    primary_url = clean_text(candidate.get("link"))
    cached_url = clean_text(candidate.get("cached_page_url"))

    has_pdf = any(x == "PDF" for x in formats) or any(looks_like_pdf(x) for x in urls)
    has_html = "HTML" in formats or bool(html_version)
    primary_direct = looks_like_direct_file(primary_url)

    fulltext_url = ""
    status = "no_fulltext_evidence"
    evidence = "none"

    if has_pdf:
        status = "open_pdf_resource"
        evidence = "google_scholar_resource_pdf"
        fulltext_url = next((x for x in urls if looks_like_pdf(x)), urls[0] if urls else "")
    elif has_html:
        status = "open_html_resource"
        evidence = "google_scholar_resource_html"
        fulltext_url = html_version or (urls[0] if urls else "")
    elif primary_direct:
        status = "direct_fulltext_primary"
        evidence = "google_scholar_primary_file"
        fulltext_url = primary_url
    elif urls:
        status = "resource_available_other"
        evidence = "google_scholar_resource_other"
        fulltext_url = urls[0]
    elif cached_url:
        status = "cached_copy_available"
        evidence = "google_scholar_cached_page"
        fulltext_url = cached_url
    elif primary_url:
        status = "landing_page_only"
        evidence = "google_scholar_primary_link_only"

    open_evidence = status in {
        "open_pdf_resource",
        "open_html_resource",
        "direct_fulltext_primary",
        "resource_available_other",
        "cached_copy_available",
    }

    return {
        "google_scholar_has_resource": bool(urls),
        "google_scholar_resource_count": len(urls),
        "google_scholar_has_pdf_resource": has_pdf,
        "google_scholar_has_html_resource": has_html,
        "google_scholar_resource_formats": " | ".join(formats),
        "google_scholar_resource_urls": " | ".join(urls),
        "google_scholar_resource_domains": " | ".join(domains),
        "google_scholar_resource_titles": " | ".join(titles),
        "google_scholar_primary_is_direct_file": primary_direct,
        "google_scholar_primary_is_pdf": looks_like_pdf(primary_url),
        "google_scholar_cached_page_available": bool(cached_url),
        "google_scholar_cached_page_url": cached_url,
        "google_scholar_fulltext_url": fulltext_url,
        "google_scholar_open_fulltext_evidence": open_evidence,
        "google_scholar_access_status": status,
        "google_scholar_access_evidence": evidence,
        "google_scholar_paywall_status": (
            "open_copy_available"
            if open_evidence
            else "not_assessable_from_google_scholar"
        ),
    }


# ============================================================
# 출력 레코드
# ============================================================

def blank_result(
    match_status: str,
    query_count: int = 0,
    cache_hits: int = 0,
    api_error: str = "",
) -> dict[str, Any]:
    return {
        "google_scholar_indexed": False,
        "google_scholar_match_status": match_status,
        "google_scholar_match_accepted": False,
        "google_scholar_match_confidence": "none",
        "google_scholar_match_score": None,
        "google_scholar_title_score": None,
        "google_scholar_author_score": None,
        "google_scholar_journal_score": None,
        "google_scholar_year_match": None,
        "google_scholar_corroboration_count": 0,
        "google_scholar_query": "",
        "google_scholar_query_source": "",
        "google_scholar_search_page": None,
        "google_scholar_search_start": None,
        "google_scholar_result_position": None,
        "google_scholar_global_result_position": None,
        "google_scholar_result_id": "",
        "google_scholar_result_type": "",
        "google_scholar_title": "",
        "google_scholar_authors": "",
        "google_scholar_author_ids": "",
        "google_scholar_publication_summary": "",
        "google_scholar_year": None,
        "google_scholar_source": "",
        "google_scholar_snippet": "",
        "google_scholar_primary_url": "",
        "google_scholar_primary_domain": "",
        "google_scholar_citation_count": None,
        "google_scholar_cites_id": "",
        "google_scholar_cited_by_url": "",
        "google_scholar_versions_count": None,
        "google_scholar_cluster_id": "",
        "google_scholar_versions_url": "",
        "google_scholar_related_pages_url": "",
        "google_scholar_has_resource": False,
        "google_scholar_resource_count": 0,
        "google_scholar_has_pdf_resource": False,
        "google_scholar_has_html_resource": False,
        "google_scholar_resource_formats": "",
        "google_scholar_resource_urls": "",
        "google_scholar_resource_domains": "",
        "google_scholar_resource_titles": "",
        "google_scholar_primary_is_direct_file": False,
        "google_scholar_primary_is_pdf": False,
        "google_scholar_cached_page_available": False,
        "google_scholar_cached_page_url": "",
        "google_scholar_fulltext_url": "",
        "google_scholar_open_fulltext_evidence": False,
        "google_scholar_access_status": "not_indexed" if match_status == "not_indexed" else "unknown",
        "google_scholar_access_evidence": "none",
        "google_scholar_paywall_status": "not_indexed" if match_status == "not_indexed" else "not_assessable_from_google_scholar",
        "google_scholar_api_status": "Error" if api_error else "",
        "google_scholar_api_error": api_error,
        "google_scholar_search_id": "",
        "google_scholar_result_count_returned": 0,
        "google_scholar_total_results_reported": None,
        "google_scholar_organic_results_state": "",
        "google_scholar_query_count_used": query_count,
        "google_scholar_local_cache_hits": cache_hits,
        "google_scholar_retrieved_at": now_utc_iso(),
    }


def candidate_to_output(
    scored: dict[str, Any],
    query_count: int,
    cache_hits: int,
    api_error: str,
) -> dict[str, Any]:
    status, confidence, accepted = classify(scored)
    candidate = scored["candidate"]

    author_names = [
        clean_text(x.get("name"))
        for x in candidate.get("authors") or []
        if isinstance(x, dict) and clean_text(x.get("name"))
    ]
    author_ids = [
        clean_text(x.get("author_id"))
        for x in candidate.get("authors") or []
        if isinstance(x, dict) and clean_text(x.get("author_id"))
    ]

    metadata = scored.get("search_metadata") or {}
    info = scored.get("search_information") or {}

    output = {
        "google_scholar_indexed": accepted,
        "google_scholar_match_status": status,
        "google_scholar_match_accepted": accepted,
        "google_scholar_match_confidence": confidence,
        "google_scholar_match_score": scored["weighted_score"],
        "google_scholar_title_score": scored["title_score"],
        "google_scholar_author_score": scored["author_score"],
        "google_scholar_journal_score": scored["journal_score"],
        "google_scholar_year_match": scored["year_match"],
        "google_scholar_corroboration_count": scored["corroboration_count"],
        "google_scholar_query": scored["query"],
        "google_scholar_query_source": scored["query_source"],
        "google_scholar_search_page": scored["search_page"],
        "google_scholar_search_start": scored["search_start"],
        "google_scholar_result_position": scored["result_position"],
        "google_scholar_global_result_position": scored["global_result_position"],
        "google_scholar_result_id": clean_text(candidate.get("result_id")),
        "google_scholar_result_type": clean_text(candidate.get("type")),
        "google_scholar_title": clean_text(candidate.get("title")),
        "google_scholar_authors": " | ".join(dict.fromkeys(author_names)),
        "google_scholar_author_ids": " | ".join(dict.fromkeys(author_ids)),
        "google_scholar_publication_summary": clean_text(candidate.get("publication_summary")),
        "google_scholar_year": scored.get("candidate_year"),
        "google_scholar_source": get_domain(candidate.get("link")),
        "google_scholar_snippet": clean_text(candidate.get("snippet")),
        "google_scholar_primary_url": clean_text(candidate.get("link")),
        "google_scholar_primary_domain": get_domain(candidate.get("link")),
        "google_scholar_citation_count": safe_int(candidate.get("citation_count")),
        "google_scholar_cites_id": clean_text(candidate.get("cites_id")),
        "google_scholar_cited_by_url": clean_text(candidate.get("cited_by_url")),
        "google_scholar_versions_count": safe_int(candidate.get("versions_count")),
        "google_scholar_cluster_id": clean_text(candidate.get("cluster_id")),
        "google_scholar_versions_url": clean_text(candidate.get("versions_url")),
        "google_scholar_related_pages_url": clean_text(candidate.get("related_pages_url")),
        "google_scholar_api_status": clean_text(metadata.get("status")),
        "google_scholar_api_error": api_error,
        "google_scholar_search_id": clean_text(metadata.get("id")),
        "google_scholar_result_count_returned": None,
        "google_scholar_total_results_reported": safe_int(info.get("total_results")),
        "google_scholar_organic_results_state": clean_text(info.get("organic_results_state")),
        "google_scholar_query_count_used": query_count,
        "google_scholar_local_cache_hits": cache_hits,
        "google_scholar_retrieved_at": now_utc_iso(),
    }

    output.update(access_metadata(candidate))

    if not accepted and status == "review":
        output["google_scholar_access_status"] = "review"
        output["google_scholar_paywall_status"] = "review"

    return output


# ============================================================
# 논문 한 편 처리
# ============================================================

def process_one_paper(
    conn: sqlite3.Connection,
    session: requests.Session,
    row: pd.Series,
) -> dict[str, Any]:
    variants = build_title_variants(row)
    if not variants:
        return blank_result("missing_search_title")

    all_candidates = []
    network_queries = 0
    cache_hits = 0
    last_error = ""
    searched = set()

    best_page1 = None
    best_page1_variant = None
    best_page1_response = None

    for variant in variants:
        if network_queries >= MAX_QUERIES_PER_PAPER:
            break

        query = exact_title_query(variant["title"])
        key = (query, 0)
        if not query or key in searched:
            continue
        searched.add(key)

        response, network_used = serpapi_search(conn, session, query, 0)
        network_queries += int(network_used)
        cache_hits += int(not network_used)
        last_error = clean_text(response.get("api_error")) or last_error

        ranked = rank_results(row, variant, query, 0, response)
        all_candidates.extend(ranked)

        current_best = ranked[0] if ranked else None
        if current_best and (
            best_page1 is None
            or current_best["weighted_score"] > best_page1["weighted_score"]
        ):
            best_page1 = current_best
            best_page1_variant = variant
            best_page1_response = response

        if current_best:
            status, confidence, accepted = classify(current_best)
            if accepted and confidence == "high":
                return candidate_to_output(
                    current_best,
                    network_queries,
                    cache_hits,
                    last_error,
                )

    overall_best = (
        max(
            all_candidates,
            key=lambda x: (
                x["weighted_score"],
                x["title_score"],
                x["corroboration_count"],
            ),
        )
        if all_candidates
        else None
    )

    if overall_best:
        _, _, accepted = classify(overall_best)
        if accepted:
            return candidate_to_output(
                overall_best,
                network_queries,
                cache_hits,
                last_error,
            )

    # 저자 제한 검색: 첫 번째 제목이 짧거나 기존 후보가 애매할 때만
    if (
        ENABLE_AUTHOR_REFINED_SEARCH
        and variants
        and network_queries < MAX_QUERIES_PER_PAPER
    ):
        first_variant = variants[0]
        title_words = len(normalize_title(first_variant["title"]).split())
        best_score = overall_best["weighted_score"] if overall_best else 0.0

        if first_variant["author"] and (title_words <= 7 or best_score < ACCEPT_WEIGHTED_SCORE):
            query = author_refined_query(first_variant["title"], first_variant["author"])
            key = (query, 0)

            if query and key not in searched:
                searched.add(key)
                response, network_used = serpapi_search(conn, session, query, 0)
                network_queries += int(network_used)
                cache_hits += int(not network_used)
                last_error = clean_text(response.get("api_error")) or last_error

                ranked = rank_results(row, first_variant, query, 0, response)
                all_candidates.extend(ranked)

                if ranked:
                    refined_best = ranked[0]
                    if overall_best is None or refined_best["weighted_score"] > overall_best["weighted_score"]:
                        overall_best = refined_best

                    _, _, accepted = classify(refined_best)
                    if accepted:
                        return candidate_to_output(
                            refined_best,
                            network_queries,
                            cache_hits,
                            last_error,
                        )

    # 선택적 두 번째 페이지
    if (
        ENABLE_SELECTIVE_SECOND_PAGE
        and network_queries < MAX_QUERIES_PER_PAPER
        and best_page1 is not None
        and best_page1_variant is not None
        and best_page1_response is not None
        and len(best_page1_response.get("organic_results") or []) == RESULTS_PER_PAGE
        and SECOND_PAGE_MIN_SCORE
        <= best_page1["weighted_score"]
        <= SECOND_PAGE_MAX_SCORE
    ):
        query = exact_title_query(best_page1_variant["title"])
        key = (query, RESULTS_PER_PAGE)

        if key not in searched:
            response, network_used = serpapi_search(
                conn,
                session,
                query,
                RESULTS_PER_PAGE,
            )
            network_queries += int(network_used)
            cache_hits += int(not network_used)
            last_error = clean_text(response.get("api_error")) or last_error

            ranked = rank_results(
                row,
                best_page1_variant,
                query,
                RESULTS_PER_PAGE,
                response,
            )
            all_candidates.extend(ranked)

    if all_candidates:
        overall_best = max(
            all_candidates,
            key=lambda x: (
                x["weighted_score"],
                x["title_score"],
                x["corroboration_count"],
                -(x["global_result_position"] if x["global_result_position"] is not None else 9999),
            ),
        )
        return candidate_to_output(
            overall_best,
            network_queries,
            cache_hits,
            last_error,
        )

    return blank_result(
        "api_error" if last_error else "not_indexed",
        network_queries,
        cache_hits,
        last_error,
    )


# ============================================================
# 행별 즉시 저장 및 재시작
# ============================================================

def completed_uids_from_output() -> set[str]:
    if not OUTPUT_FILE.exists() or OUTPUT_FILE.stat().st_size == 0:
        return set()

    try:
        existing = pd.read_csv(
            OUTPUT_FILE,
            usecols=["paper_uid_after_direct_w"],
            dtype=str,
            encoding="utf-8-sig",
            low_memory=False,
        )
    except (ValueError, pd.errors.EmptyDataError):
        return set()

    return set(
        existing["paper_uid_after_direct_w"]
        .fillna("")
        .astype(str)
        .str.strip()
        .loc[lambda x: x.ne("")]
    )


def append_row_immediately(row: pd.Series, result: dict[str, Any]) -> None:
    original = {
        str(k): v
        for k, v in row.to_dict().items()
        if not str(k).startswith("google_scholar_")
    }
    record = {**original, **result}

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0

    # DictWriter를 사용해 열 순서를 첫 행에서 고정한다.
    fieldnames = list(record.keys())

    if file_exists:
        with open(OUTPUT_FILE, "r", encoding="utf-8-sig", newline="") as rf:
            reader = csv.reader(rf)
            existing_header = next(reader, [])
        if existing_header:
            fieldnames = existing_header

    with open(
        OUTPUT_FILE,
        "a",
        encoding="utf-8-sig" if not file_exists else "utf-8",
        newline="",
    ) as wf:
        writer = csv.DictWriter(wf, fieldnames=fieldnames, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: record.get(k, "") for k in fieldnames})
        wf.flush()
        os.fsync(wf.fileno())


# ============================================================
# 데이터 준비
# ============================================================

def ensure_optional_columns(df: pd.DataFrame) -> pd.DataFrame:
    optional = [
        "ref_author",
        "ref_publisher_or_journal",
        "ref_year",
        "kci_title_original",
        "kci_title_english",
        "kci_authors_korean",
        "kci_authors_english",
        "kci_journal_name",
        "kci_pub_year",
        "search_journal_name",
        "search_pub_year",
    ]

    for col in optional:
        if col not in df.columns:
            df[col] = ""

    return df



def has_text(series: pd.Series) -> pd.Series:
    return (
        series.fillna("")
        .astype(str)
        .str.strip()
        .replace({"nan": "", "None": "", "<NA>": ""})
        .ne("")
    )


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    전체 데이터에서 테스트용 10개를 고정 추출한다.
    영어 KCI 제목 보유 5개와 미보유 5개를 우선 구성한다.
    """
    searchable = (
        has_text(df["kci_title_english"])
        | has_text(df["kci_title_original"])
        | has_text(df["ref_title"])
    )

    eligible = (
        df.loc[searchable]
        .drop_duplicates(subset=["paper_uid_after_direct_w"], keep="first")
        .copy()
    )

    english_mask = has_text(eligible["kci_title_english"])
    english_pool = eligible.loc[english_mask]
    non_english_pool = eligible.loc[~english_mask]

    english_sample = english_pool.sample(
        n=min(5, len(english_pool)),
        random_state=20260719,
    )

    non_english_sample = non_english_pool.sample(
        n=min(5, len(non_english_pool)),
        random_state=20260720,
    )

    test_df = pd.concat(
        [english_sample, non_english_sample],
        ignore_index=True,
    )

    if len(test_df) < 10:
        selected = set(test_df["paper_uid_after_direct_w"].astype(str))
        remaining = eligible.loc[
            ~eligible["paper_uid_after_direct_w"].astype(str).isin(selected)
        ]
        needed = min(10 - len(test_df), len(remaining))
        if needed > 0:
            test_df = pd.concat(
                [
                    test_df,
                    remaining.sample(n=needed, random_state=20260721),
                ],
                ignore_index=True,
            )

    test_df = (
        test_df.sample(frac=1, random_state=20260722)
        .head(10)
        .reset_index(drop=True)
    )
    test_df.insert(0, "google_scholar_test_order", range(1, len(test_df) + 1))

    sample_file = BASE_DIR / "rq2analticsample_google_scholar_test10_sample.csv"
    test_df.to_csv(sample_file, index=False, encoding="utf-8-sig")
    print(f"테스트 표본 저장: {sample_file}")

    return test_df



# ============================================================
# 메인
# ============================================================

def main() -> None:
    if SERPAPI_KEY == "123":
        print("주의: SERPAPI_KEY가 예시값 '123'입니다. 실제 키로 교체하세요.")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"입력 파일이 없습니다: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig", low_memory=False)
    df = ensure_optional_columns(df)
    df = prepare_dataframe(df)

    required = ["paper_uid_after_direct_w", "ref_title"]
    missing = [x for x in required if x not in df.columns]
    if missing:
        raise KeyError(f"필수 열이 없습니다: {missing}")

    if df["paper_uid_after_direct_w"].duplicated().any():
        raise ValueError("paper_uid_after_direct_w에 중복값이 있습니다.")

    completed = completed_uids_from_output()
    rows = df[
        ~df["paper_uid_after_direct_w"].astype(str).isin(completed)
    ].copy()

    print("=" * 80)
    print("Google Scholar 테스트 10개 수집")
    print("=" * 80)
    print(f"입력 파일: {INPUT_FILE}")
    print(f"출력 파일: {OUTPUT_FILE}")
    print(f"전체 대상: {len(df):,}")
    print(f"기존 완료: {len(completed):,}")
    print(f"이번 실행: {len(rows):,}")
    print()

    conn = open_cache_db()
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 GoogleScholarMetadataResearch/1.0",
            "Accept": "application/json",
        }
    )

    processed = 0

    try:
        for _, row in rows.iterrows():
            uid = clean_text(row["paper_uid_after_direct_w"])
            if not uid:
                continue

            try:
                result = process_one_paper(conn, session, row)
            except Exception as exc:
                message = f"paper_uid={uid}, {type(exc).__name__}: {exc}"
                log_error(message)
                result = blank_result("processing_error", api_error=message)

            # 논문 한 편이 끝날 때마다 즉시 디스크 저장
            append_row_immediately(row, result)
            processed += 1

            print(
                f"[{processed:,}/{len(rows):,}] "
                f"UID={uid} | "
                f"status={result.get('google_scholar_match_status')} | "
                f"score={result.get('google_scholar_match_score')} | "
                f"queries={result.get('google_scholar_query_count_used')} | "
                f"citations={result.get('google_scholar_citation_count')} | "
                f"access={result.get('google_scholar_access_status')}"
            )

    except KeyboardInterrupt:
        print("\n중단되었습니다. 이미 처리된 행은 출력 CSV에 저장되어 있습니다.")

    finally:
        session.close()
        conn.close()

    print()
    print(f"이번 실행에서 저장한 논문 수: {processed:,}")
    print(f"결과 파일: {OUTPUT_FILE}")



# ============================================================
# 실제 원문 접근 검증: Google Scholar 링크를 직접 열어 확인
# ============================================================

from bs4 import BeautifulSoup
from urllib.parse import urljoin

ACCESS_REQUEST_TIMEOUT_SECONDS = 30
ACCESS_MAX_HTML_BYTES = 2_000_000
ACCESS_MAX_FILE_PROBE_BYTES = 1_048_576
ACCESS_MAX_DOWNLOAD_CANDIDATES = 6

DOWNLOAD_TEXT_PATTERN = re.compile(
    r"(pdf|download|full\s*text|fulltext|원문|다운로드|전문|파일\s*받기|논문\s*보기)",
    re.IGNORECASE,
)
DOWNLOAD_HREF_PATTERN = re.compile(
    r"(pdf|download|filedown|file_down|downfile|fulltext|full_text|articlefile|viewfile|attach)",
    re.IGNORECASE,
)
BLOCK_TEXT_PATTERN = re.compile(
    r"(login|log\s*in|sign\s*in|institutional\s*access|subscribe|subscription|"
    r"purchase|payment|paywall|unauthorized|forbidden|access\s*denied|"
    r"로그인|기관\s*인증|구독|결제|구매|권한이\s*없|접근이\s*제한|원문이용|"
    r"소속기관|인증\s*후|회원만|유료)",
    re.IGNORECASE,
)


def _new_access_fields() -> dict[str, Any]:
    return {
        "google_scholar_fulltext_access": "",
        "google_scholar_access_verified": False,
        "google_scholar_link_provided": False,
        "google_scholar_landing_url": "",
        "google_scholar_landing_http_status": None,
        "google_scholar_landing_final_url": "",
        "google_scholar_landing_content_type": "",
        "google_scholar_download_link_found": False,
        "google_scholar_download_url": "",
        "google_scholar_download_http_status": None,
        "google_scholar_download_final_url": "",
        "google_scholar_download_content_type": "",
        "google_scholar_download_content_disposition": "",
        "google_scholar_download_verified": False,
        "google_scholar_access_block_reason": "",
        "google_scholar_access_verification_error": "",
        "google_scholar_access_http_request_count": 0,
        "google_scholar_access_verified_at": "",
        "google_scholar_cached_page_available": False,
        "google_scholar_cached_page_url": "",
        "google_scholar_best_candidate_title": "",
        "google_scholar_best_candidate_url": "",
        "google_scholar_best_candidate_score": None,
    }


def _response_probe(response: requests.Response) -> tuple[bytes, str, str]:
    content_type = clean_text(response.headers.get("Content-Type")).lower()
    disposition = clean_text(response.headers.get("Content-Disposition")).lower()

    chunks = []
    total = 0
    limit = (
        ACCESS_MAX_HTML_BYTES
        if "html" in content_type or "text/" in content_type
        else ACCESS_MAX_FILE_PROBE_BYTES
    )

    for chunk in response.iter_content(chunk_size=65536):
        if not chunk:
            continue
        remaining = limit - total
        if remaining <= 0:
            break
        chunks.append(chunk[:remaining])
        total += len(chunks[-1])
        if total >= limit:
            break

    return b"".join(chunks), content_type, disposition


def _is_open_file(
    body: bytes,
    content_type: str,
    disposition: str,
    final_url: str,
) -> bool:
    prefix = body[:16]
    return (
        prefix.startswith(b"%PDF-")
        or "application/pdf" in content_type
        or "application/octet-stream" in content_type
        and "attachment" in disposition
        or "attachment" in disposition
        and len(body) > 0
        or looks_like_direct_file(final_url)
        and "text/html" not in content_type
        and "application/xhtml" not in content_type
    )


def _html_text(body: bytes, response: requests.Response) -> str:
    encoding = response.encoding or response.apparent_encoding or "utf-8"
    try:
        return body.decode(encoding, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def _looks_blocked(
    status_code: int,
    final_url: str,
    html: str,
) -> tuple[bool, str]:
    if status_code in {401, 402, 403, 407, 451}:
        return True, f"http_{status_code}"

    lowered_url = final_url.lower()
    if any(x in lowered_url for x in ("login", "signin", "auth", "paywall", "purchase")):
        return True, "redirected_to_auth_or_payment"

    sample = html[:300_000]
    if BLOCK_TEXT_PATTERN.search(sample):
        return True, "login_payment_or_institutional_access_required"

    return False, ""


def _extract_download_candidates(
    html: str,
    base_url: str,
) -> tuple[list[str], bool]:
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []
    control_found = False

    for element in soup.find_all(["a", "button", "input"]):
        text = " ".join(
            [
                clean_text(element.get_text(" ", strip=True)),
                clean_text(element.get("title")),
                clean_text(element.get("aria-label")),
                clean_text(element.get("value")),
            ]
        )
        href = clean_text(element.get("href"))
        onclick = clean_text(element.get("onclick"))

        text_match = bool(DOWNLOAD_TEXT_PATTERN.search(text))
        href_match = bool(DOWNLOAD_HREF_PATTERN.search(href))
        onclick_match = bool(DOWNLOAD_HREF_PATTERN.search(onclick))

        if text_match or href_match or onclick_match:
            control_found = True

        if href and (text_match or href_match):
            absolute = urljoin(base_url, href)
            if absolute.startswith(("http://", "https://")):
                urls.append(absolute)

        if onclick and (text_match or onclick_match):
            matches = re.findall(
                r"""['"]((?:https?://|/)[^'"]+)['"]""",
                onclick,
                flags=re.IGNORECASE,
            )
            for match in matches:
                absolute = urljoin(base_url, match)
                if absolute.startswith(("http://", "https://")):
                    urls.append(absolute)

    return list(dict.fromkeys(urls))[:ACCESS_MAX_DOWNLOAD_CANDIDATES], control_found


def _request_and_probe(
    session: requests.Session,
    url: str,
    referer: str = "",
) -> dict[str, Any]:
    headers = {
        "Accept": "application/pdf,text/html,application/xhtml+xml,application/octet-stream;q=0.9,*/*;q=0.8",
    }
    if referer:
        headers["Referer"] = referer

    response = session.get(
        url,
        headers=headers,
        timeout=ACCESS_REQUEST_TIMEOUT_SECONDS,
        allow_redirects=True,
        stream=True,
    )
    try:
        body, content_type, disposition = _response_probe(response)
        final_url = clean_text(response.url)
        html = (
            _html_text(body, response)
            if "html" in content_type or body.lstrip().startswith((b"<!DOCTYPE", b"<html", b"<?xml"))
            else ""
        )
        return {
            "status_code": response.status_code,
            "final_url": final_url,
            "content_type": content_type,
            "content_disposition": disposition,
            "body": body,
            "html": html,
            "is_open_file": _is_open_file(
                body,
                content_type,
                disposition,
                final_url,
            ),
        }
    finally:
        response.close()


def verify_fulltext_access(candidate: dict[str, Any]) -> dict[str, Any]:
    """
    SerpAPI 검색 결과에 포함된 외부 링크를 일반 HTTP 요청으로 직접 검증한다.
    이 요청들은 SerpAPI 검색 쿼리를 증가시키지 않는다.
    """
    result = _new_access_fields()
    result["google_scholar_access_verified_at"] = now_utc_iso()
    result["google_scholar_cached_page_available"] = bool(
        clean_text(candidate.get("cached_page_url"))
    )
    result["google_scholar_cached_page_url"] = clean_text(
        candidate.get("cached_page_url")
    )

    primary_url = clean_text(candidate.get("link"))
    resources = candidate.get("resources") or []
    html_version = clean_text(candidate.get("html_version"))

    candidate_links: list[tuple[str, str]] = []
    for resource in resources:
        if not isinstance(resource, dict):
            continue
        url = clean_text(resource.get("link"))
        if url:
            candidate_links.append(("scholar_resource", url))

    if html_version:
        candidate_links.append(("scholar_html_version", html_version))
    if primary_url:
        candidate_links.append(("scholar_primary", primary_url))

    deduped: list[tuple[str, str]] = []
    seen_urls: set[str] = set()
    for source, url in candidate_links:
        if url not in seen_urls:
            seen_urls.add(url)
            deduped.append((source, url))

    result["google_scholar_link_provided"] = bool(deduped)
    if not deduped:
        result["google_scholar_fulltext_access"] = "no_link_provided"
        result["google_scholar_access_verified"] = True
        return result

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/149.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        }
    )

    landing_seen = False
    download_control_seen = False
    blocked_reason = ""
    verification_errors: list[str] = []

    try:
        for source, url in deduped:
            try:
                probe = _request_and_probe(session, url)
                result["google_scholar_access_http_request_count"] += 1
            except requests.RequestException as exc:
                verification_errors.append(
                    f"{source}:{type(exc).__name__}:{exc}"
                )
                continue

            if not landing_seen:
                landing_seen = True
                result["google_scholar_landing_url"] = url
                result["google_scholar_landing_http_status"] = probe["status_code"]
                result["google_scholar_landing_final_url"] = probe["final_url"]
                result["google_scholar_landing_content_type"] = probe["content_type"]

            if probe["is_open_file"] and 200 <= probe["status_code"] < 400:
                result.update(
                    {
                        "google_scholar_fulltext_access": "direct_fulltext_open",
                        "google_scholar_access_verified": True,
                        "google_scholar_download_url": url,
                        "google_scholar_download_http_status": probe["status_code"],
                        "google_scholar_download_final_url": probe["final_url"],
                        "google_scholar_download_content_type": probe["content_type"],
                        "google_scholar_download_content_disposition": probe[
                            "content_disposition"
                        ],
                        "google_scholar_download_verified": True,
                    }
                )
                return result

            blocked, reason = _looks_blocked(
                probe["status_code"],
                probe["final_url"],
                probe["html"],
            )
            if blocked and not blocked_reason:
                blocked_reason = reason

            if not probe["html"]:
                continue

            download_urls, control_found = _extract_download_candidates(
                probe["html"],
                probe["final_url"],
            )
            download_control_seen = download_control_seen or control_found

            if control_found:
                result["google_scholar_download_link_found"] = True

            if control_found and not download_urls:
                blocked_reason = blocked_reason or "download_control_has_no_resolvable_url"

            for download_url in download_urls:
                result["google_scholar_download_link_found"] = True
                if not result["google_scholar_download_url"]:
                    result["google_scholar_download_url"] = download_url

                try:
                    download_probe = _request_and_probe(
                        session,
                        download_url,
                        referer=probe["final_url"],
                    )
                    result["google_scholar_access_http_request_count"] += 1
                except requests.RequestException as exc:
                    verification_errors.append(
                        f"download:{type(exc).__name__}:{exc}"
                    )
                    continue

                result["google_scholar_download_http_status"] = download_probe[
                    "status_code"
                ]
                result["google_scholar_download_final_url"] = download_probe[
                    "final_url"
                ]
                result["google_scholar_download_content_type"] = download_probe[
                    "content_type"
                ]
                result["google_scholar_download_content_disposition"] = (
                    download_probe["content_disposition"]
                )

                if (
                    download_probe["is_open_file"]
                    and 200 <= download_probe["status_code"] < 400
                ):
                    result.update(
                        {
                            "google_scholar_fulltext_access": "download_link_open",
                            "google_scholar_access_verified": True,
                            "google_scholar_download_url": download_url,
                            "google_scholar_download_verified": True,
                            "google_scholar_access_block_reason": "",
                        }
                    )
                    return result

                download_blocked, download_reason = _looks_blocked(
                    download_probe["status_code"],
                    download_probe["final_url"],
                    download_probe["html"],
                )
                if download_blocked:
                    blocked_reason = download_reason

        result["google_scholar_access_verified"] = True

        if download_control_seen:
            result["google_scholar_fulltext_access"] = "download_link_blocked"
            result["google_scholar_access_block_reason"] = (
                blocked_reason or "download_did_not_return_an_open_file"
            )
        elif blocked_reason:
            result["google_scholar_fulltext_access"] = "page_blocked"
            result["google_scholar_access_block_reason"] = blocked_reason
        elif landing_seen:
            result["google_scholar_fulltext_access"] = "landing_page_only"
        else:
            result["google_scholar_fulltext_access"] = "verification_error"
            result["google_scholar_access_verified"] = False

        if verification_errors:
            result["google_scholar_access_verification_error"] = " | ".join(
                verification_errors
            )[:4000]

        return result

    finally:
        session.close()


_BASE_BLANK_RESULT = blank_result


def blank_result(
    match_status: str,
    query_count: int = 0,
    cache_hits: int = 0,
    api_error: str = "",
) -> dict[str, Any]:
    output = _BASE_BLANK_RESULT(
        match_status,
        query_count,
        cache_hits,
        api_error,
    )
    output.update(_new_access_fields())
    output["google_scholar_fulltext_access"] = (
        "not_indexed"
        if match_status in {"not_indexed", "no_result"}
        else "not_verified"
    )
    return output


_BASE_CANDIDATE_TO_OUTPUT = candidate_to_output


def candidate_to_output(
    scored: dict[str, Any],
    query_count: int,
    cache_hits: int,
    api_error: str,
) -> dict[str, Any]:
    """
    확정 매칭된 논문에 대해서만 인용·서지·접근 변수를 저장한다.
    미확정 후보는 진단 변수에만 남긴다.
    """
    output = _BASE_CANDIDATE_TO_OUTPUT(
        scored,
        query_count,
        cache_hits,
        api_error,
    )
    candidate = scored["candidate"]
    accepted = bool(output.get("google_scholar_match_accepted"))

    output.update(_new_access_fields())
    output["google_scholar_cached_page_available"] = bool(
        clean_text(candidate.get("cached_page_url"))
    )
    output["google_scholar_cached_page_url"] = clean_text(
        candidate.get("cached_page_url")
    )

    if not accepted:
        output["google_scholar_best_candidate_title"] = clean_text(
            candidate.get("title")
        )
        output["google_scholar_best_candidate_url"] = clean_text(
            candidate.get("link")
        )
        output["google_scholar_best_candidate_score"] = scored.get(
            "weighted_score"
        )

        # 오답 후보의 값을 실제 논문 변수로 저장하지 않는다.
        clear_fields = [
            "google_scholar_result_id",
            "google_scholar_result_type",
            "google_scholar_title",
            "google_scholar_authors",
            "google_scholar_author_ids",
            "google_scholar_publication_summary",
            "google_scholar_year",
            "google_scholar_source",
            "google_scholar_snippet",
            "google_scholar_primary_url",
            "google_scholar_primary_domain",
            "google_scholar_citation_count",
            "google_scholar_cites_id",
            "google_scholar_cited_by_url",
            "google_scholar_versions_count",
            "google_scholar_cluster_id",
            "google_scholar_versions_url",
            "google_scholar_related_pages_url",
            "google_scholar_has_resource",
            "google_scholar_resource_count",
            "google_scholar_has_pdf_resource",
            "google_scholar_has_html_resource",
            "google_scholar_resource_formats",
            "google_scholar_resource_urls",
            "google_scholar_resource_domains",
            "google_scholar_resource_titles",
            "google_scholar_primary_is_direct_file",
            "google_scholar_primary_is_pdf",
            "google_scholar_fulltext_url",
            "google_scholar_open_fulltext_evidence",
        ]
        for field in clear_fields:
            output[field] = (
                False
                if field in {
                    "google_scholar_has_resource",
                    "google_scholar_has_pdf_resource",
                    "google_scholar_has_html_resource",
                    "google_scholar_primary_is_direct_file",
                    "google_scholar_primary_is_pdf",
                    "google_scholar_open_fulltext_evidence",
                }
                else 0
                if field == "google_scholar_resource_count"
                else None
                if field in {
                    "google_scholar_citation_count",
                    "google_scholar_versions_count",
                    "google_scholar_year",
                }
                else ""
            )

        output["google_scholar_fulltext_access"] = (
            "review_not_verified"
            if output.get("google_scholar_match_status") == "review"
            else "not_indexed"
        )
        output["google_scholar_access_status"] = output[
            "google_scholar_fulltext_access"
        ]
        output["google_scholar_paywall_status"] = "not_assessed"
        return output

    verified = verify_fulltext_access(candidate)
    output.update(verified)

    # 이전 코드의 추정 기반 변수를 실제 검증 결과로 덮어쓴다.
    output["google_scholar_access_status"] = output[
        "google_scholar_fulltext_access"
    ]
    output["google_scholar_open_fulltext_evidence"] = (
        output["google_scholar_fulltext_access"]
        in {"direct_fulltext_open", "download_link_open"}
    )
    output["google_scholar_fulltext_url"] = (
        output["google_scholar_download_final_url"]
        or output["google_scholar_download_url"]
    )
    output["google_scholar_paywall_status"] = (
        "open_copy_verified"
        if output["google_scholar_download_verified"]
        else "blocked_or_not_open"
        if output["google_scholar_fulltext_access"]
        in {"download_link_blocked", "page_blocked"}
        else "no_open_fulltext_found"
        if output["google_scholar_fulltext_access"] == "landing_page_only"
        else "verification_inconclusive"
    )

    return output


# ============================================================
# KCI 우선 매칭 규칙
# ============================================================

def _kci_only_first_nonempty(
    row: pd.Series,
    columns: list[str],
) -> str:
    """지정된 KCI 칼럼 안에서만 첫 번째 유효값을 반환한다."""
    for column in columns:
        value = clean_text(row.get(column))
        if value:
            return value
    return ""


def build_title_variants(
    row: pd.Series,
) -> list[dict[str, str]]:
    """
    검색 및 매칭 기준 선택 규칙

    1. KCI 영어 제목 또는 KCI 원문 제목이 하나라도 있으면:
       - KCI 제목, KCI 저자, KCI 연도, KCI 저널만 사용
       - ref_* 변수는 사용하지 않음

    2. KCI 영어 제목과 KCI 원문 제목이 모두 없으면:
       - ref_title, ref_author, ref_year,
         ref_publisher_or_journal 사용
    """
    kci_english_title = clean_text(
        row.get("kci_title_english")
    )
    kci_original_title = clean_text(
        row.get("kci_title_original")
    )

    kci_english_author = _kci_only_first_nonempty(
        row,
        [
            "kci_authors_english",
            "kci_author_english",
            "kci_author_name_english",
            # 영어 저자가 없을 때도 KCI 저자 안에서만 fallback
            "kci_authors_korean",
            "kci_author_korean",
            "kci_author_name_korean",
        ],
    )

    kci_korean_author = _kci_only_first_nonempty(
        row,
        [
            "kci_authors_korean",
            "kci_author_korean",
            "kci_author_name_korean",
            # 한국어 저자가 없을 때도 KCI 저자 안에서만 fallback
            "kci_authors_english",
            "kci_author_english",
            "kci_author_name_english",
        ],
    )

    kci_year = _kci_only_first_nonempty(
        row,
        [
            "kci_pub_year",
            "kci_year",
            "kci_publication_year",
            "kci_issue_year",
        ],
    )

    kci_journal = _kci_only_first_nonempty(
        row,
        [
            "kci_journal_name",
            "kci_journal_name_original",
            "kci_journal_title",
            "kci_journal",
        ],
    )

    if kci_english_title or kci_original_title:
        candidates = [
            {
                "title": kci_english_title,
                "author": kci_english_author,
                "year": kci_year,
                "journal": kci_journal,
                "source": "kci_english",
                "metadata_source": "kci",
            },
            {
                "title": kci_original_title,
                "author": kci_korean_author,
                "year": kci_year,
                "journal": kci_journal,
                "source": "kci_original",
                "metadata_source": "kci",
            },
        ]
    else:
        candidates = [
            {
                "title": clean_text(row.get("ref_title")),
                "author": clean_text(row.get("ref_author")),
                "year": clean_text(row.get("ref_year")),
                "journal": clean_text(
                    row.get("ref_publisher_or_journal")
                ),
                "source": "reference",
                "metadata_source": "reference",
            }
        ]

    variants: list[dict[str, str]] = []
    seen_titles: set[str] = set()

    for item in candidates:
        normalized_title = normalize_title(
            item["title"]
        ).replace(" ", "")

        if not normalized_title:
            continue

        if normalized_title in seen_titles:
            continue

        seen_titles.add(normalized_title)
        variants.append(item)

    return variants


def score_candidate(
    row: pd.Series,
    variant: dict[str, str],
    candidate: dict[str, Any],
    query: str,
    start: int,
    response: dict[str, Any],
) -> dict[str, Any]:
    """
    매칭점수:
      제목 72%
      저자 15%
      연도 9%
      저널 4%

    각 점수는 현재 검색 variant에 포함된 동일 출처의 메타데이터로 계산한다.
    KCI variant이면 네 요소 모두 KCI 정보이며 ref_*는 사용하지 않는다.
    """
    title_score = title_similarity(
        variant.get("title"),
        candidate.get("title"),
    )

    author_score = author_similarity(
        variant.get("author"),
        candidate.get("authors") or [],
        clean_text(candidate.get("publication_summary")),
    )

    expected_year = extract_year(
        variant.get("year")
    )
    candidate_year = extract_year(
        candidate.get("publication_summary")
    )

    year_match = (
        expected_year == candidate_year
        if expected_year is not None
        and candidate_year is not None
        else None
    )

    expected_journal = normalize_title(
        variant.get("journal")
    )
    publication_summary = normalize_title(
        candidate.get("publication_summary")
    )

    journal_score = (
        float(
            max(
                fuzz.partial_ratio(
                    expected_journal,
                    publication_summary,
                ),
                fuzz.token_set_ratio(
                    expected_journal,
                    publication_summary,
                ),
            )
        )
        if expected_journal and publication_summary
        else None
    )

    score_parts: list[tuple[float, float]] = [
        (title_score, 0.72)
    ]

    if author_score is not None:
        score_parts.append(
            (author_score, 0.15)
        )

    if year_match is not None:
        score_parts.append(
            (
                100.0 if year_match else 0.0,
                0.09,
            )
        )

    if journal_score is not None:
        score_parts.append(
            (journal_score, 0.04)
        )

    weighted_score = (
        sum(score * weight for score, weight in score_parts)
        / sum(weight for _, weight in score_parts)
    )

    position = safe_int(
        candidate.get("position")
    )
    global_position = (
        start + position
        if position is not None
        else None
    )

    corroboration_count = 0

    if (
        author_score is not None
        and author_score >= 70
    ):
        corroboration_count += 1

    if year_match is True:
        corroboration_count += 1

    if (
        journal_score is not None
        and journal_score >= 70
    ):
        corroboration_count += 1

    return {
        "candidate": candidate,
        "query": query,
        "query_source": variant.get("source", ""),
        "match_metadata_source": variant.get(
            "metadata_source",
            "",
        ),
        "match_input_title": clean_text(
            variant.get("title")
        ),
        "match_input_author": clean_text(
            variant.get("author")
        ),
        "match_input_year": expected_year,
        "match_input_journal": clean_text(
            variant.get("journal")
        ),
        "search_start": start,
        "search_page": (
            start // RESULTS_PER_PAGE + 1
        ),
        "result_position": position,
        "global_result_position": global_position,
        "title_score": round(
            title_score,
            4,
        ),
        "author_score": (
            round(author_score, 4)
            if author_score is not None
            else None
        ),
        "journal_score": (
            round(journal_score, 4)
            if journal_score is not None
            else None
        ),
        "year_match": year_match,
        "candidate_year": candidate_year,
        "corroboration_count": corroboration_count,
        "weighted_score": round(
            weighted_score,
            4,
        ),
        "search_metadata": (
            response.get("search_metadata")
            or {}
        ),
        "search_information": (
            response.get("search_information")
            or {}
        ),
    }


_KCI_BASE_CANDIDATE_TO_OUTPUT = candidate_to_output


def candidate_to_output(
    scored: dict[str, Any],
    query_count: int,
    cache_hits: int,
    api_error: str,
) -> dict[str, Any]:
    output = _KCI_BASE_CANDIDATE_TO_OUTPUT(
        scored,
        query_count,
        cache_hits,
        api_error,
    )

    output.update(
        {
            "google_scholar_match_metadata_source": (
                scored.get("match_metadata_source", "")
            ),
            "google_scholar_match_input_title": (
                scored.get("match_input_title", "")
            ),
            "google_scholar_match_input_author": (
                scored.get("match_input_author", "")
            ),
            "google_scholar_match_input_year": (
                scored.get("match_input_year")
            ),
            "google_scholar_match_input_journal": (
                scored.get("match_input_journal", "")
            ),
        }
    )

    return output


# ============================================================
# 최종 수정:
# 1) SerpAPI의 "검색 결과 없음" 메시지는 API 오류가 아니라 no-result로 처리
# 2) 로그인/기관인증 문구가 페이지에 존재한다는 이유만으로 blocked 처리하지 않음
# 3) 실제 HTTP 상태, 인증 URL 리디렉션, 다운로드 요청 결과로만 blocked 판정
# 4) 직접 파일 판정을 더 보수적으로 적용
# ============================================================

_NO_RESULT_ERROR_PATTERNS = (
    "google hasn't returned any results",
    "google has not returned any results",
    "no results for this query",
    "no results found",
    "did not return any results",
)


def _is_no_result_message(value: Any) -> bool:
    text = clean_text(value).lower()
    return bool(
        text
        and any(pattern in text for pattern in _NO_RESULT_ERROR_PATTERNS)
    )


_BASE_FINAL_SERPAPI_SEARCH = serpapi_search


def serpapi_search(
    conn: sqlite3.Connection,
    session: requests.Session,
    query: str,
    start: int = 0,
) -> tuple[dict[str, Any], bool]:
    """
    SerpAPI가 정상 응답했지만 검색 결과가 없다고 알리는 경우에는
    api_error를 비운다. 그러면 최종 상태는 api_error가 아니라
    not_indexed로 저장된다.
    """
    payload, network_used = _BASE_FINAL_SERPAPI_SEARCH(
        conn,
        session,
        query,
        start,
    )

    if _is_no_result_message(payload.get("api_error")):
        payload = dict(payload)
        payload["api_error"] = ""

        search_information = dict(
            payload.get("search_information") or {}
        )
        if not clean_text(
            search_information.get("organic_results_state")
        ):
            search_information["organic_results_state"] = "No results"
        payload["search_information"] = search_information
        payload["organic_results"] = []

    return payload, network_used


def _is_open_file(
    body: bytes,
    content_type: str,
    disposition: str,
    final_url: str,
) -> bool:
    """
    URL이 .pdf처럼 보인다는 이유만으로 파일 접근 성공으로 판정하지 않는다.
    실제 응답 본문 또는 HTTP 헤더가 파일임을 뒷받침해야 한다.
    """
    normalized_content_type = clean_text(content_type).lower()
    normalized_disposition = clean_text(disposition).lower()
    prefix = body[:16].lstrip()

    if prefix.startswith(b"%PDF-"):
        return True

    if "application/pdf" in normalized_content_type and len(body) > 0:
        return True

    is_html = (
        "text/html" in normalized_content_type
        or "application/xhtml" in normalized_content_type
        or prefix.startswith((b"<!DOCTYPE", b"<html", b"<?xml"))
    )
    if is_html:
        return False

    if (
        "attachment" in normalized_disposition
        and len(body) > 0
        and (
            "filename=" in normalized_disposition
            or "application/octet-stream" in normalized_content_type
            or "application/zip" in normalized_content_type
            or "application/msword" in normalized_content_type
            or "officedocument" in normalized_content_type
        )
    ):
        return True

    return False


def _looks_blocked(
    status_code: int,
    final_url: str,
    html: str,
) -> tuple[bool, str]:
    """
    blocked는 명시적인 HTTP 차단 또는 인증·결제 페이지로의 실제
    리디렉션이 확인된 경우에만 판정한다.

    페이지 본문에 로그인, 기관인증, 구독 문구가 단순히 포함된 것은
    blocked의 근거로 사용하지 않는다.
    """
    if status_code in {401, 402, 403, 407, 451}:
        return True, f"http_{status_code}"

    lowered_url = clean_text(final_url).lower()
    auth_path_patterns = (
        "/login",
        "/signin",
        "/sign-in",
        "/auth/",
        "/authenticate",
        "/sso/",
        "/paywall",
        "/purchase",
        "/payment",
        "/subscribe",
    )

    if any(pattern in lowered_url for pattern in auth_path_patterns):
        return True, "redirected_to_auth_or_payment"

    return False, ""


def verify_fulltext_access(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """
    Scholar가 제공한 링크를 실제 HTTP 요청으로 검증한다.

    분류:
    - direct_fulltext_open:
      Scholar 대표/리소스 URL 자체가 실제 파일 응답
    - download_link_open:
      랜딩페이지의 다운로드 URL 요청이 실제 파일 응답
    - download_link_blocked:
      다운로드 URL을 실제 요청한 뒤 HTTP 차단 또는 인증/결제
      URL로의 리디렉션이 확인됨
    - download_link_unverified:
      다운로드 컨트롤/URL은 있으나 실제 파일 또는 명시적 차단을
      확인하지 못함
    - page_blocked:
      대표 페이지 요청 자체가 HTTP 차단 또는 인증/결제 URL로 리디렉션
    - landing_page_only:
      페이지는 열리지만 검증 가능한 다운로드 링크가 없음
    """
    result = _new_access_fields()
    result["google_scholar_access_verified_at"] = now_utc_iso()
    result["google_scholar_cached_page_available"] = bool(
        clean_text(candidate.get("cached_page_url"))
    )
    result["google_scholar_cached_page_url"] = clean_text(
        candidate.get("cached_page_url")
    )

    primary_url = clean_text(candidate.get("link"))
    resources = candidate.get("resources") or []
    html_version = clean_text(candidate.get("html_version"))

    candidate_links: list[tuple[str, str]] = []

    for resource in resources:
        if not isinstance(resource, dict):
            continue
        resource_url = clean_text(resource.get("link"))
        if resource_url:
            candidate_links.append(
                ("scholar_resource", resource_url)
            )

    if html_version:
        candidate_links.append(
            ("scholar_html_version", html_version)
        )

    if primary_url:
        candidate_links.append(
            ("scholar_primary", primary_url)
        )

    deduped: list[tuple[str, str]] = []
    seen_urls: set[str] = set()

    for source, url in candidate_links:
        if url and url not in seen_urls:
            seen_urls.add(url)
            deduped.append((source, url))

    result["google_scholar_link_provided"] = bool(deduped)

    if not deduped:
        result["google_scholar_fulltext_access"] = "no_link_provided"
        result["google_scholar_access_verified"] = True
        return result

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/149.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        }
    )

    landing_seen = False
    page_explicitly_blocked = False
    page_block_reason = ""

    download_control_seen = False
    download_url_seen = False
    download_request_made = False
    download_explicitly_blocked = False
    download_block_reason = ""

    verification_errors: list[str] = []

    try:
        for source, url in deduped:
            try:
                probe = _request_and_probe(
                    session,
                    url,
                )
                result[
                    "google_scholar_access_http_request_count"
                ] += 1
            except requests.RequestException as exc:
                verification_errors.append(
                    f"{source}:{type(exc).__name__}:{exc}"
                )
                continue

            if not landing_seen:
                landing_seen = True
                result["google_scholar_landing_url"] = url
                result[
                    "google_scholar_landing_http_status"
                ] = probe["status_code"]
                result[
                    "google_scholar_landing_final_url"
                ] = probe["final_url"]
                result[
                    "google_scholar_landing_content_type"
                ] = probe["content_type"]

            if (
                probe["is_open_file"]
                and 200 <= probe["status_code"] < 400
            ):
                result.update(
                    {
                        "google_scholar_fulltext_access": (
                            "direct_fulltext_open"
                        ),
                        "google_scholar_access_verified": True,
                        "google_scholar_download_url": url,
                        "google_scholar_download_http_status": (
                            probe["status_code"]
                        ),
                        "google_scholar_download_final_url": (
                            probe["final_url"]
                        ),
                        "google_scholar_download_content_type": (
                            probe["content_type"]
                        ),
                        "google_scholar_download_content_disposition": (
                            probe["content_disposition"]
                        ),
                        "google_scholar_download_verified": True,
                        "google_scholar_access_block_reason": "",
                    }
                )
                return result

            blocked, reason = _looks_blocked(
                probe["status_code"],
                probe["final_url"],
                probe["html"],
            )

            if blocked:
                page_explicitly_blocked = True
                if not page_block_reason:
                    page_block_reason = reason

            if not probe["html"]:
                continue

            download_urls, control_found = (
                _extract_download_candidates(
                    probe["html"],
                    probe["final_url"],
                )
            )

            download_control_seen = (
                download_control_seen or control_found
            )

            if control_found:
                result[
                    "google_scholar_download_link_found"
                ] = True

            for download_url in download_urls:
                download_url_seen = True
                download_request_made = True
                result[
                    "google_scholar_download_link_found"
                ] = True

                if not result["google_scholar_download_url"]:
                    result[
                        "google_scholar_download_url"
                    ] = download_url

                try:
                    download_probe = _request_and_probe(
                        session,
                        download_url,
                        referer=probe["final_url"],
                    )
                    result[
                        "google_scholar_access_http_request_count"
                    ] += 1
                except requests.RequestException as exc:
                    verification_errors.append(
                        f"download:{type(exc).__name__}:{exc}"
                    )
                    continue

                result[
                    "google_scholar_download_http_status"
                ] = download_probe["status_code"]
                result[
                    "google_scholar_download_final_url"
                ] = download_probe["final_url"]
                result[
                    "google_scholar_download_content_type"
                ] = download_probe["content_type"]
                result[
                    "google_scholar_download_content_disposition"
                ] = download_probe["content_disposition"]

                if (
                    download_probe["is_open_file"]
                    and 200 <= download_probe["status_code"] < 400
                ):
                    result.update(
                        {
                            "google_scholar_fulltext_access": (
                                "download_link_open"
                            ),
                            "google_scholar_access_verified": True,
                            "google_scholar_download_url": (
                                download_url
                            ),
                            "google_scholar_download_verified": True,
                            "google_scholar_access_block_reason": "",
                        }
                    )
                    return result

                (
                    download_blocked,
                    download_reason,
                ) = _looks_blocked(
                    download_probe["status_code"],
                    download_probe["final_url"],
                    download_probe["html"],
                )

                if download_blocked:
                    download_explicitly_blocked = True
                    if not download_block_reason:
                        download_block_reason = download_reason

        result["google_scholar_access_verified"] = True

        if download_explicitly_blocked:
            result[
                "google_scholar_fulltext_access"
            ] = "download_link_blocked"
            result[
                "google_scholar_access_block_reason"
            ] = download_block_reason

        elif download_control_seen or download_url_seen:
            # 다운로드 기능은 보였지만 실제 파일도 명시적 차단도 확인되지 않음
            result[
                "google_scholar_fulltext_access"
            ] = "download_link_unverified"
            result[
                "google_scholar_access_block_reason"
            ] = (
                "download_request_did_not_return_verified_file"
                if download_request_made
                else "download_control_has_no_resolvable_url"
            )

        elif page_explicitly_blocked:
            result[
                "google_scholar_fulltext_access"
            ] = "page_blocked"
            result[
                "google_scholar_access_block_reason"
            ] = page_block_reason

        elif landing_seen:
            result[
                "google_scholar_fulltext_access"
            ] = "landing_page_only"

        else:
            result[
                "google_scholar_fulltext_access"
            ] = "verification_error"
            result[
                "google_scholar_access_verified"
            ] = False

        if verification_errors:
            result[
                "google_scholar_access_verification_error"
            ] = " | ".join(
                verification_errors
            )[:4000]

        return result

    finally:
        session.close()


# ============================================================
# 분석용 0/1 변수
# ============================================================

def _to_binary(value: Any) -> int:
    """불리언·숫자·문자 값을 명시적인 0/1 정수로 변환한다."""
    if isinstance(value, str):
        return int(value.strip().lower() in {"1", "true", "yes", "y"})
    return int(bool(value))


def add_analysis_access_flags(
    output: dict[str, Any],
) -> dict[str, Any]:
    """
    복잡한 접근성 진단 필드에서 분석용 0/1 변수를 생성한다.

    google_scholar_indexed
        정확한 Scholar 매칭이 수락되었으면 1.

    google_scholar_fulltext_link_provided
        Scholar 결과 또는 연결된 랜딩페이지에서 원문 파일·HTML 원문·
        다운로드 링크/컨트롤이 확인되었으면 1.
        단순 서지 랜딩페이지와 cached page는 포함하지 않는다.

    google_scholar_oa_link_provided
        로그인·결제 없이 실제 원문 파일 응답이 확인된 링크가 있으면 1.

    google_scholar_restricted_link_provided
        원문 후보 링크를 요청했으나 HTTP 차단, 로그인, 기관인증,
        SSO 또는 결제 페이지로의 리디렉션이 확인되었으면 1.

    google_scholar_open_fulltext
        실제 원문 파일 다운로드가 검증되었으면 1.
    """
    accepted = bool(
        output.get("google_scholar_match_accepted")
    )
    access_status = clean_text(
        output.get("google_scholar_fulltext_access")
    )

    verified_open = bool(
        accepted
        and output.get("google_scholar_download_verified")
        and access_status
        in {"direct_fulltext_open", "download_link_open"}
    )

    restricted = bool(
        accepted
        and access_status
        in {"download_link_blocked", "page_blocked"}
    )

    # 단순 대표 서지 페이지는 제외한다.
    # Scholar resource, HTML version, 직접 파일, 또는 실제 페이지에서
    # 발견된 다운로드 링크/컨트롤만 원문 링크 제공으로 본다.
    candidate_fulltext_link = bool(
        accepted
        and (
            output.get("google_scholar_has_resource")
            or output.get("google_scholar_has_pdf_resource")
            or output.get("google_scholar_has_html_resource")
            or output.get("google_scholar_primary_is_direct_file")
            or output.get("google_scholar_download_link_found")
            or clean_text(
                output.get("google_scholar_download_url")
            )
            or access_status
            in {
                "direct_fulltext_open",
                "download_link_open",
                "download_link_blocked",
                "download_link_unverified",
            }
        )
    )

    output["google_scholar_indexed"] = int(accepted)
    output[
        "google_scholar_fulltext_link_provided"
    ] = int(candidate_fulltext_link)
    output[
        "google_scholar_oa_link_provided"
    ] = int(verified_open)
    output[
        "google_scholar_restricted_link_provided"
    ] = int(restricted)
    output[
        "google_scholar_open_fulltext"
    ] = int(verified_open)

    return output


_PRE_ANALYSIS_BLANK_RESULT = blank_result


def blank_result(
    match_status: str,
    query_count: int = 0,
    cache_hits: int = 0,
    api_error: str = "",
) -> dict[str, Any]:
    output = _PRE_ANALYSIS_BLANK_RESULT(
        match_status,
        query_count,
        cache_hits,
        api_error,
    )
    return add_analysis_access_flags(output)


_PRE_ANALYSIS_CANDIDATE_TO_OUTPUT = candidate_to_output


def candidate_to_output(
    scored: dict[str, Any],
    query_count: int,
    cache_hits: int,
    api_error: str,
) -> dict[str, Any]:
    output = _PRE_ANALYSIS_CANDIDATE_TO_OUTPUT(
        scored,
        query_count,
        cache_hits,
        api_error,
    )
    return add_analysis_access_flags(output)


# ============================================================
# 잘못된 다운로드 후보 링크 제외
# ============================================================

INVALID_FULLTEXT_HOSTS = {
    "chrome.google.com",
    "chromewebstore.google.com",
    "addons.mozilla.org",
    "apps.apple.com",
    "play.google.com",
}

INVALID_FULLTEXT_URL_TERMS = {
    "chrome-extension",
    "browser-extension",
    "webstore",
    "app-store",
    "/addons/",
    "/addon/",
    "/extensions/",
}


def _is_valid_fulltext_candidate_url(url: Any) -> bool:
    """
    논문 원문과 무관한 브라우저 확장 프로그램·앱스토어 URL을 제외한다.
    """
    cleaned = clean_text(url)
    if not cleaned:
        return False

    try:
        parsed = urlparse(cleaned)
    except Exception:
        return False

    host = (parsed.hostname or "").lower()
    lowered = cleaned.lower()

    if host in INVALID_FULLTEXT_HOSTS:
        return False

    if any(term in lowered for term in INVALID_FULLTEXT_URL_TERMS):
        return False

    return parsed.scheme in {"http", "https"}


def _extract_download_candidates(
    html: str,
    base_url: str,
) -> tuple[list[str], bool]:
    """
    랜딩페이지에서 실제 원문 다운로드 후보만 추출한다.

    브라우저 확장 프로그램, 앱스토어 링크 등은 URL 후보에서도 제외하고
    다운로드 컨트롤 존재 여부에도 반영하지 않는다. 반면 href가 없는
    실제 다운로드 버튼은 unresolved control로 유지한다.
    """
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []
    control_found = False

    for element in soup.find_all(["a", "button", "input"]):
        text = " ".join(
            [
                clean_text(element.get_text(" ", strip=True)),
                clean_text(element.get("title")),
                clean_text(element.get("aria-label")),
                clean_text(element.get("value")),
            ]
        )
        href = clean_text(element.get("href"))
        onclick = clean_text(element.get("onclick"))

        text_match = bool(DOWNLOAD_TEXT_PATTERN.search(text))
        href_match = bool(DOWNLOAD_HREF_PATTERN.search(href))
        onclick_match = bool(DOWNLOAD_HREF_PATTERN.search(onclick))

        element_matched = text_match or href_match or onclick_match
        if not element_matched:
            continue

        valid_urls_for_element: list[str] = []

        if href and (text_match or href_match):
            absolute = urljoin(base_url, href)
            if _is_valid_fulltext_candidate_url(absolute):
                valid_urls_for_element.append(absolute)

        if onclick and (text_match or onclick_match):
            matches = re.findall(
                r"""['"]((?:https?://|/)[^'"]+)['"]""",
                onclick,
                flags=re.IGNORECASE,
            )
            for match in matches:
                absolute = urljoin(base_url, match)
                if _is_valid_fulltext_candidate_url(absolute):
                    valid_urls_for_element.append(absolute)

        if valid_urls_for_element:
            control_found = True
            urls.extend(valid_urls_for_element)
            continue

        # 링크 URL이 아예 없는 버튼/입력 요소는 실제 다운로드 컨트롤일
        # 가능성이 있으므로 unresolved control로 보존한다.
        has_any_embedded_url = bool(href or onclick)
        if not has_any_embedded_url and element.name in {"button", "input"}:
            control_found = True

    return list(dict.fromkeys(urls))[:ACCESS_MAX_DOWNLOAD_CANDIDATES], control_found


def add_analysis_access_flags(
    output: dict[str, Any],
) -> dict[str, Any]:
    """
    접근성 진단 결과에서 분석용 0/1 변수를 생성한다.
    """
    accepted = bool(
        output.get("google_scholar_match_accepted")
    )
    access_status = clean_text(
        output.get("google_scholar_fulltext_access")
    )

    verified_open = bool(
        accepted
        and output.get("google_scholar_download_verified")
        and access_status
        in {"direct_fulltext_open", "download_link_open"}
    )

    restricted = bool(
        accepted
        and access_status
        in {"download_link_blocked", "page_blocked"}
    )

    download_url = clean_text(
        output.get("google_scholar_download_url")
    )
    valid_download_url = bool(
        download_url
        and _is_valid_fulltext_candidate_url(download_url)
    )

    candidate_fulltext_link = bool(
        accepted
        and (
            output.get("google_scholar_has_resource")
            or output.get("google_scholar_has_pdf_resource")
            or output.get("google_scholar_has_html_resource")
            or output.get("google_scholar_primary_is_direct_file")
            or (
                output.get("google_scholar_download_link_found")
                and (
                    valid_download_url
                    or access_status
                    in {
                        "download_link_open",
                        "download_link_blocked",
                        "download_link_unverified",
                    }
                )
            )
            or valid_download_url
            or access_status
            in {
                "direct_fulltext_open",
                "download_link_open",
                "download_link_blocked",
            }
            or (
                access_status == "download_link_unverified"
                and output.get("google_scholar_download_link_found")
                and (
                    valid_download_url
                    or clean_text(
                        output.get(
                            "google_scholar_access_block_reason"
                        )
                    )
                    == "download_control_has_no_resolvable_url"
                )
            )
        )
    )

    output["google_scholar_indexed"] = int(accepted)
    output[
        "google_scholar_fulltext_link_provided"
    ] = int(candidate_fulltext_link)
    output[
        "google_scholar_oa_link_provided"
    ] = int(verified_open)
    output[
        "google_scholar_restricted_link_provided"
    ] = int(restricted)
    output[
        "google_scholar_open_fulltext"
    ] = int(verified_open)

    return output


# ============================================================
# 엄격한 full-text link 정의
# ============================================================

def add_analysis_access_flags(
    output: dict[str, Any],
) -> dict[str, Any]:
    """
    분석용 접근성 0/1 변수.

    google_scholar_fulltext_link_provided = 1 은 아래 중 하나일 때만 허용한다.
      1) Scholar resource가 PDF 또는 HTML 원문으로 표시됨
      2) Scholar가 제공한 URL 자체가 직접 파일 URL임
      3) 랜딩페이지에서 실제 다운로드 버튼 또는 유효한 파일 URL이 확인됨

    출판사/DBpia의 단순 article detail·abstract·bibliographic landing page는
    full-text link로 간주하지 않는다.
    """
    accepted = bool(output.get("google_scholar_match_accepted"))
    access_status = clean_text(
        output.get("google_scholar_fulltext_access")
    )
    block_reason = clean_text(
        output.get("google_scholar_access_block_reason")
    )

    download_url = clean_text(
        output.get("google_scholar_download_url")
    )
    valid_download_url = bool(
        download_url
        and _is_valid_fulltext_candidate_url(download_url)
    )

    scholar_pdf_or_html_resource = bool(
        output.get("google_scholar_has_pdf_resource")
        or output.get("google_scholar_has_html_resource")
    )

    scholar_direct_file = bool(
        output.get("google_scholar_primary_is_direct_file")
    )

    # 실제 다운로드 버튼은 확인됐지만 JavaScript 등으로 URL만 해석하지
    # 못한 경우를 포함한다. 단순 상세페이지 URL은 포함하지 않는다.
    unresolved_real_download_control = bool(
        output.get("google_scholar_download_link_found")
        and block_reason == "download_control_has_no_resolvable_url"
    )

    verified_or_restricted_download_candidate = bool(
        valid_download_url
        and access_status
        in {
            "download_link_open",
            "download_link_blocked",
            "download_link_unverified",
        }
    )

    candidate_fulltext_link = bool(
        accepted
        and (
            scholar_pdf_or_html_resource
            or scholar_direct_file
            or valid_download_url
            or unresolved_real_download_control
            or verified_or_restricted_download_candidate
            or access_status == "direct_fulltext_open"
        )
    )

    verified_open = bool(
        accepted
        and output.get("google_scholar_download_verified")
        and access_status
        in {"direct_fulltext_open", "download_link_open"}
    )

    restricted = bool(
        candidate_fulltext_link
        and access_status
        in {"download_link_blocked", "page_blocked"}
    )

    output["google_scholar_indexed"] = int(accepted)
    output[
        "google_scholar_fulltext_link_provided"
    ] = int(candidate_fulltext_link)
    output[
        "google_scholar_oa_link_provided"
    ] = int(verified_open)
    output[
        "google_scholar_restricted_link_provided"
    ] = int(restricted)
    output[
        "google_scholar_open_fulltext"
    ] = int(verified_open)

    return output

if __name__ == "__main__":
    main()
