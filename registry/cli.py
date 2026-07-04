import argparse
from pathlib import Path

from .sources import REGISTRY_SOURCES, list_sources
from .verify import verify_dataset, verify_all


def cmd_list():
    print(f"BRF Registry -- {len(list_sources())} datasets\n")
    for key in list_sources():
        source = REGISTRY_SOURCES[key]
        print(f"  {key:<20} {source.display_name:<45} "
              f"N={source.n_samples:>5d}  G={source.n_groups:>4d}")


def cmd_download(key=None, all_=False):
    keys = list_sources() if all_ else ([key] if key else [])
    if not keys:
        print("Usage: download <key> or download --all")
        return
    for k in keys:
        source = REGISTRY_SOURCES.get(k)
        if source is None:
            print(f"  Unknown dataset: {k}")
            continue
        print(f"Downloading {k} ({source.display_name})...")
        try:
            path = source.download()
            print(f"  -> {path}")
            if source.sha256 and isinstance(path, Path):
                if not source._check_sha256(path):
                    print(f"  WARNING: SHA-256 mismatch!")
        except Exception as e:
            print(f"  FAILED: {e}")


def cmd_verify(key=None, all_=False):
    if all_:
        verify_all()
    elif key:
        verify_dataset(key)
    else:
        print("Usage: verify <key> or verify --all")


def cmd_sync():
    print("Syncing all datasets...")
    for key in list_sources():
        source = REGISTRY_SOURCES[key]
        print(f"\n  [{key}] {source.display_name}")
        try:
            path = source.download()
            print(f"    Downloaded to {path}")
            if source.sha256 and isinstance(path, Path):
                ok = source._check_sha256(path)
                print(f"    Checksum: {'OK' if ok else 'FAIL'}")
        except Exception as e:
            print(f"    FAILED: {e}")


def cmd_info(key):
    source = REGISTRY_SOURCES.get(key)
    if source is None:
        print(f"Unknown dataset: {key}")
        return
    for k, v in source.metadata().items():
        print(f"  {k}: {v}")


def main():
    parser = argparse.ArgumentParser(description="BRF Registry CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list")
    dl = sub.add_parser("download")
    dl.add_argument("key", nargs="?")
    dl.add_argument("--all", action="store_true")
    vf = sub.add_parser("verify")
    vf.add_argument("key", nargs="?")
    vf.add_argument("--all", action="store_true")
    sub.add_parser("sync")
    info = sub.add_parser("info")
    info.add_argument("key")

    args = parser.parse_args()
    if args.command == "list":
        cmd_list()
    elif args.command == "download":
        cmd_download(key=args.key, all_=args.all)
    elif args.command == "verify":
        cmd_verify(key=args.key, all_=args.all)
    elif args.command == "sync":
        cmd_sync()
    elif args.command == "info":
        cmd_info(args.key)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
