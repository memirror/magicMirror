# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/5/27

import os
import json
from hashlib import md5
from urllib.parse import urljoin, urlsplit
from dataclasses import dataclass

# pip install oss2
import oss2

from magicmirror.root import root


@dataclass
class Aliyun:
    access_key_id: str
    access_key_secret: str
    endpoint: str
    bucket_name: str


class UploadToAliyun(Aliyun):
    parent = "magicmirror/image"

    use_cache = True
    cache_path = root.parent.joinpath("aliyun", "cache", "cache.json")

    def __init__(self):
        self.bucket = oss2.Bucket(
            oss2.Auth(self.access_key_id, self.access_key_secret),
            self.endpoint,
            self.bucket_name
        )
        self.url = urljoin(self.endpoint, self.parent)
        self.record = {} if not self.use_cache else self._load_cache
        self.new_num = 0

        self._create_aliyun_cache_dir()

    def _create_aliyun_cache_dir(self):
        if not os.path.exists(self.cache_path.parent):
            os.makedirs(self.cache_path.parent)

    @property
    def _load_cache(self):
        if not os.path.exists(self.cache_path):
            return {}
        with open(self.cache_path, encoding="utf-8") as file:
            return json.load(file)

    def _perist_cache(self, force: bool = False):
        if self.new_num or force:
            with open(self.cache_path, "w", encoding="utf-8") as file:
                json.dump(self.record, file, ensure_ascii=False)

    def md5(self, name):
        name, *suffix = name.rsplit(".", maxsplit=1)
        name = md5(name.encode("utf-8")).hexdigest()
        name = ".".join([name] + suffix)
        return name

    def upload_img(self, filename) -> str:
        if not filename:
            return ""
        key = self.parent + "/" + self.md5(filename)

        if key not in self.record:
            self.bucket.put_object_from_file(key, filename)
            endpoint = urlsplit(self.endpoint)
            url = "https://" + ".".join([self.bucket_name, endpoint.netloc])
            url = urljoin(url, key)
            self.record[key] = url
            self.new_num += 1
        return self.record[key]

    def upload_imgs(self, filenames) -> dict:
        record = {}
        for filename in filenames:
            url = self.upload_img(filename)
            record[filename] = url
        self._perist_cache(force=False)
        return record
   
