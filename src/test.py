from geocoder.db.rocksdb import RocksDbGeocode
import time
import shutil
from geocoder.Geocoder import Geocoder

DB_NAME = "db/current"


if __name__ == "__main__":
    db = RocksDbGeocode(DB_NAME, create_if_missing=False)

    geocoder = Geocoder(db)

    with open(
        "test/testfiles/필수test.txt",
        "r",
        encoding="utf8",
    ) as f:
        n = 0
        errcnt = 0
        start_time = time.time()

        for line in f:
            address = line.strip()
            if address == "":
                break
            elif address.startswith("#"):  # 주석
                print(address)
                continue

            n = n + 1

            print("===============================================")
            val = geocoder.search(address)

            if not val["success"]:
                errcnt = errcnt + 1
                # continue

            print(val["address"])
            if val["errmsg"]:
                print(val["errmsg"])
            print(val["hash"])
            print(val["addressCls"])
            print(val["toksString"])

        elapsed_time = time.time() - start_time
        print(
            "total count=",
            n,
            " elapsed_time(s)=",
            elapsed_time,
            " count/sec= ",
            n / elapsed_time,
        )
        print(f"err={errcnt}, success={(n-errcnt)/n*100:2.2f}%")
