# ddns_cloudflare

## 简介：
一个简单的轮子，ddns on cloudflare 的最小化实现。

## 使用方法：

1. 将域名托管在 cloudflare.com 上， 并在 cloudflare 中获取   
对应此域名的 API 令牌，拿到对应的 dns zone id 和 token

2. 更改脚本中的以下字段：  
    ddns_domain = 'your-domain.com'   
    dns_zone_id = 'your-dns-zone-id'   
    dns_zone_token = 'your-dns-zone-token'   

3. 在 crontab 添加定时任务即可：   
    00 * * * * /usr/bin/python ddns_cloudflare.py > /var/log/ddns.log   
    //此例是每小时检测一次，具体频次可自定，但考虑到dns生效有延迟，不建议过于频繁（如小于5分钟）。

