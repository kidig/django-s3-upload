import pytest

from s3upload.utils import get_s3_path_from_url, get_bucket_endpoint_url

TEST_BUCKET = "test-bucket-name"
TEST_KEY = "folder1/folder2/file1.json"
TEST_REGION = "test-region"


@pytest.mark.parametrize(
    "url",
    [
        f"s3://{TEST_BUCKET}/{TEST_KEY}",
        f"https://{TEST_BUCKET}.s3.aws-region.amazonaws.com/{TEST_KEY}?test=1&test1=2",
        f"https://{TEST_BUCKET}.s3.amazonaws.com:443/{TEST_KEY}",
        f"https://s3-aws-region.amazonaws.com/{TEST_BUCKET}/{TEST_KEY}",
        f"https://s3-aws-region.amazonaws.com:443/{TEST_BUCKET}/{TEST_KEY}",
        f"https%3a%2f%2fs3-aws-region.amazonaws.com%3a443%2f{TEST_BUCKET}%2ffolder1%2ffolder2%2ffile1.json",
    ],
)
def test_get_s3_path_from_url(url: str) -> None:
    assert get_s3_path_from_url(url, bucket_name=TEST_BUCKET) == TEST_KEY


@pytest.mark.parametrize(
    "url,expected",
    [
        (None, f"https://{TEST_BUCKET}.s3.{TEST_REGION}.amazonaws.com"),
        ("https://{bucket}.s3.{region}.amazonaws.com", f"https://{TEST_BUCKET}.s3.{TEST_REGION}.amazonaws.com"),
        ("https://s3.{region}.amazonaws.com", f"https://s3.{TEST_REGION}.amazonaws.com"),
        ("https://{bucket}.s3.amazonaws.com", f"https://{TEST_BUCKET}.s3.amazonaws.com"),
    ]
)
def test_get_bucket_endpoint_url(url: str, expected: str) -> None:
    kwargs = {}
    if url:
        kwargs["default"] = url
    assert get_bucket_endpoint_url(bucket_name=TEST_BUCKET, region=TEST_REGION, **kwargs) == expected
