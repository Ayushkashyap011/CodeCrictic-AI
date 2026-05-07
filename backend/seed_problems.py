#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_problems.py
Seed MongoDB with problems from data/problems.json.

Usage:
    python seed_problems.py                  # uses .env
    python seed_problems.py --drop           # drop existing problems first
    python seed_problems.py --json path.json # custom dataset file
"""
import asyncio
import json
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

# Fix Unicode on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Allow running from the backend/ directory
sys.path.insert(0, str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "codecritic")
COLLECTION = "problems"
DEFAULT_JSON = Path(__file__).parent / "data" / "problems.json"


async def seed(json_path: Path, drop: bool = False) -> None:
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    col = db[COLLECTION]

    # Verify connection
    await client.admin.command("ping")
    print(f"✅ Connected to MongoDB: {MONGODB_URL}/{DATABASE_NAME}")

    if drop:
        await col.drop()
        print("🗑  Dropped existing problems collection")

    with open(json_path, "r", encoding="utf-8") as f:
        problems: list[dict] = json.load(f)

    print(f"📂 Loaded {len(problems)} problems from {json_path}")

    inserted = 0
    skipped = 0
    for problem in problems:
        # Skip duplicates by slug
        existing = await col.find_one({"slug": problem["slug"]})
        if existing:
            skipped += 1
            continue

        problem["created_at"] = datetime.utcnow()
        problem.setdefault("total_submissions", 0)
        problem.setdefault("accepted_submissions", 0)
        await col.insert_one(problem)
        inserted += 1
        print(f"  ✓ {problem['title']} [{problem['difficulty']}]")

    # Create indexes for fast lookups
    await col.create_index("slug", unique=True)
    await col.create_index("difficulty")
    await col.create_index("category")
    await col.create_index([("title", "text")])

    print(f"\n🎉 Seeding complete: {inserted} inserted, {skipped} skipped")
    client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed CodeCritic MongoDB")
    parser.add_argument(
        "--drop", action="store_true", help="Drop existing problems before seeding"
    )
    parser.add_argument(
        "--json", type=Path, default=DEFAULT_JSON, help="Path to problems JSON file"
    )
    args = parser.parse_args()

    if not args.json.exists():
        print(f"❌ JSON file not found: {args.json}")
        sys.exit(1)

    asyncio.run(seed(args.json, args.drop))


if __name__ == "__main__":
    main()
