#!/usr/bin/env python3
"""
MinIO File Downloader Script

This script downloads files from a specified MinIO bucket to a local directory.
It supports filtering by file extensions, recursive downloads, and progress tracking.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Set
from urllib.parse import urlparse

from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

# ---! Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("minio_download.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

env_path = os.getenv("ENV_PATH")
if env_path is None:
    raise ValueError("ENV_PATH is not set")

load_dotenv(env_path)

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")


class MinIODownloader:
    """Handles downloading files from MinIO buckets"""

    def __init__(self):
        """
        Initialize MinIO client

        Args:
            endpoint: MinIO server endpoint (e.g., 'localhost:9000')
            access_key: MinIO access key
            secret_key: MinIO secret key
            secure: Whether to use HTTPS (default: True)
        """
        self.client = Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )
        logger.info(f"Initialized MinIO client for endpoint: {MINIO_ENDPOINT}")

    def list_buckets(self) -> List[str]:
        """List all available buckets"""
        try:
            buckets = self.client.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]
            logger.info(f"Available buckets: {bucket_names}")
            return bucket_names
        except S3Error as e:
            logger.error(f"Error listing buckets: {e}")
            return []

    def list_objects(
        self, bucket_name: str, prefix: str = "", recursive: bool = True
    ) -> List[str]:
        """
        List objects in a bucket with optional prefix filtering

        Args:
            bucket_name: Name of the bucket
            prefix: Prefix to filter objects (optional)
            recursive: Whether to list recursively (default: True)

        Returns:
            List of object names
        """
        try:
            objects = self.client.list_objects(
                bucket_name, prefix=prefix, recursive=recursive
            )
            object_names = [obj.object_name for obj in objects]
            logger.info(
                f"Found {len(object_names)} objects in bucket '{bucket_name}' with prefix '{prefix}'"
            )
            return object_names
        except S3Error as e:
            logger.error(f"Error listing objects in bucket '{bucket_name}': {e}")
            return []

    def download_file(
        self, bucket_name: str, object_name: str, local_path: str
    ) -> bool:
        """
        Download a single file from MinIO to local storage

        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object in the bucket
            local_path: Local file path to save to

        Returns:
            True if successful, False otherwise
        """
        try:
            # ---! Ensure local directory exists
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)

            # ---! Download the file
            self.client.fget_object(bucket_name, object_name, local_path)
            logger.info(f"Downloaded: {object_name} -> {local_path}")
            return True

        except S3Error as e:
            logger.error(f"Error downloading {object_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error downloading {object_name}: {e}")
            return False

    def download_bucket_contents(
        self,
        bucket_name: str,
        local_dir: str,
        prefix: str = "",
        extensions: Optional[Set[str]] = None,
        recursive: bool = True,
        max_files: Optional[int] = None,
    ) -> dict:
        """
        Download multiple files from a bucket

        Args:
            bucket_name: Name of the bucket
            local_dir: Local directory to save files
            prefix: Prefix to filter objects (optional)
            extensions: Set of file extensions to include (optional)
            recursive: Whether to download recursively (default: True)
            max_files: Maximum number of files to download (optional)

        Returns:
            Dictionary with download statistics
        """
        # ---! Ensure local directory exists
        os.makedirs(local_dir, exist_ok=True)

        # ---! Get list of objects
        objects = self.list_objects(bucket_name, prefix, recursive)

        if not objects:
            logger.warning(
                f"No objects found in bucket '{bucket_name}' with prefix '{prefix}'"
            )
            return {"total": 0, "downloaded": 0, "failed": 0, "skipped": 0}

        # ---! Filter by extensions if specified
        if extensions:
            filtered_objects = []
            for obj in objects:
                file_ext = Path(obj).suffix.lower()
                if file_ext in extensions or file_ext.replace(".", "") in extensions:
                    filtered_objects.append(obj)
            objects = filtered_objects
            logger.info(
                f"Filtered to {len(objects)} objects with extensions: {extensions}"
            )

        # ---! Limit number of files if specified
        if max_files and len(objects) > max_files:
            objects = objects[:max_files]
            logger.info(f"Limited to {max_files} files")

        # ---! Download files
        downloaded = 0
        failed = 0
        skipped = 0

        for i, object_name in enumerate(objects, 1):
            logger.info(f"Processing file {i}/{len(objects)}: {object_name}")

            # ---! Determine local file path
            if prefix and object_name.startswith(prefix):
                relative_path = object_name[len(prefix) :].lstrip("/")
            else:
                relative_path = object_name

            local_path = os.path.join(local_dir, relative_path)

            # ---! Skip if file already exists
            if os.path.exists(local_path):
                logger.info(f"Skipping existing file: {local_path}")
                skipped += 1
                continue

            # ---! Download the file
            if self.download_file(bucket_name, object_name, local_path):
                downloaded += 1
            else:
                failed += 1

        # ---! Return statistics
        stats = {
            "total": len(objects),
            "downloaded": downloaded,
            "failed": failed,
            "skipped": skipped,
        }

        logger.info(f"Download complete. Stats: {stats}")
        return stats


def load_config_from_env() -> dict:
    """Load MinIO configuration from environment variables"""
    config = {
        "endpoint": os.getenv("MINIO_ENDPOINT"),
        "access_key": os.getenv("MINIO_ACCESS_KEY"),
        "secret_key": os.getenv("MINIO_SECRET_KEY"),
        "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
        "bucket": os.getenv("MINIO_BUCKET"),
        "local_dir": os.getenv("MINIO_LOCAL_DIR", "./downloads"),
    }

    # ---! Check required configuration
    missing = [
        key for key, value in config.items() if value is None and key != "local_dir"
    ]
    if missing:
        logger.error(f"Missing required environment variables: {missing}")
        logger.error("Please set the following environment variables:")
        logger.error("  MINIO_ENDPOINT - MinIO server endpoint (e.g., localhost:9000)")
        logger.error("  MINIO_ACCESS_KEY - MinIO access key")
        logger.error("  MINIO_SECRET_KEY - MinIO secret key")
        logger.error("  MINIO_BUCKET - Bucket name to download from")
        logger.error("  MINIO_SECURE - Whether to use HTTPS (default: true)")
        logger.error(
            "  MINIO_LOCAL_DIR - Local directory for downloads (default: ./downloads)"
        )
        return None

    return config


def main_old():
    """Main function to handle command line arguments and execute downloads"""
    parser = argparse.ArgumentParser(description="Download files from MinIO bucket")
    parser.add_argument("--bucket", help="MinIO bucket name")
    parser.add_argument("--local-dir", help="Local directory to save files")
    parser.add_argument("--prefix", help="Prefix to filter objects")
    parser.add_argument("--extensions", nargs="+", help="File extensions to include")
    parser.add_argument(
        "--recursive", action="store_true", default=True, help="Download recursively"
    )
    parser.add_argument(
        "--max-files", type=int, help="Maximum number of files to download"
    )
    parser.add_argument(
        "--list-buckets", action="store_true", help="List available buckets"
    )
    parser.add_argument(
        "--list-objects", action="store_true", help="List objects in bucket"
    )
    parser.add_argument("--endpoint", help="MinIO server endpoint")
    parser.add_argument("--access-key", help="MinIO access key")
    parser.add_argument("--secret-key", help="MinIO secret key")
    parser.add_argument("--secure", action="store_true", default=True, help="Use HTTPS")

    args = parser.parse_args()

    # ---! Load configuration
    config = load_config_from_env()
    if not config:
        sys.exit(1)

    # ---! Override config with command line arguments
    if args.endpoint:
        config["endpoint"] = args.endpoint
    if args.access_key:
        config["access_key"] = args.access_key
    if args.secret_key:
        config["secret_key"] = args.secret_key
    if args.bucket:
        config["bucket"] = args.bucket
    if args.local_dir:
        config["local_dir"] = args.local_dir

    # ---! Initialize MinIO client
    try:
        downloader = MinIODownloader(
            config["endpoint"],
            config["access_key"],
            config["secret_key"],
            config["secure"],
        )
    except Exception as e:
        logger.error(f"Failed to initialize MinIO client: {e}")
        sys.exit(1)

    # ---! Handle list operations
    if args.list_buckets:
        buckets = downloader.list_buckets()
        if buckets:
            print("\nAvailable buckets:")
            for bucket in buckets:
                print(f"  - {bucket}")
        return

    if args.list_objects:
        if not config["bucket"]:
            logger.error("Bucket name required for listing objects")
            sys.exit(1)

        objects = downloader.list_objects(
            config["bucket"], args.prefix or "", args.recursive
        )
        if objects:
            print(f"\nObjects in bucket '{config['bucket']}':")
            for obj in objects:
                print(f"  - {obj}")
        return

    # ---! Validate bucket name
    if not config["bucket"]:
        logger.error(
            "Bucket name is required. Use --bucket or set MINIO_BUCKET environment variable."
        )
        sys.exit(1)

    # ---! Check if bucket exists
    try:
        if not downloader.client.bucket_exists(config["bucket"]):
            logger.error(f"Bucket '{config['bucket']}' does not exist")
            sys.exit(1)
    except S3Error as e:
        logger.error(f"Error checking bucket existence: {e}")
        sys.exit(1)

    # ---! Prepare extensions filter
    extensions = None
    if args.extensions:
        extensions = {
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in args.extensions
        }

    # ---! Execute download
    logger.info(
        f"Starting download from bucket '{config['bucket']}' to '{config['local_dir']}'"
    )

    stats = downloader.download_bucket_contents(
        bucket_name=config["bucket"],
        local_dir=config["local_dir"],
        prefix=args.prefix or "",
        extensions=extensions,
        recursive=args.recursive,
        max_files=args.max_files,
    )

    # ---! Print summary
    print("\n" + "=" * 50)
    print("DOWNLOAD SUMMARY")
    print("=" * 50)
    print(f"Bucket: {config['bucket']}")
    print(f"Local Directory: {config['local_dir']}")
    print(f"Total Files: {stats['total']}")
    print(f"Downloaded: {stats['downloaded']}")
    print(f"Failed: {stats['failed']}")
    print(f"Skipped: {stats['skipped']}")
    print("=" * 50)

    if stats["failed"] > 0:
        sys.exit(1)


def main():
    minioHandler = MinIODownloader()
    buckets = minioHandler.list_buckets()
    minioHandler.download_bucket_contents(
        bucket_name="call-center-insight",
        local_dir="./calls",
        prefix="",
        extensions={".json"},
        recursive=True,
    )


if __name__ == "__main__":
    main()
