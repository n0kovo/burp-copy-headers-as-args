# Burp Extension: Copy Headers As -H Arguments

## Description

The "Copy Headers As -H Arguments" Burp Suite extension adds a new context menu entry that will copy the headers from the selected request to the clipboard, in the following format:

```-H "Host:example.com" -H "Cache-Control:max-age=0" -H "Upgrade-Insecure-Requests:1" -H "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36" -H "Sec-Gpc:1" -H "Sec-Fetch-Site:none" -H "Sec-Fetch-Mode:navigate" -H "Sec-Fetch-User:?1" -H "Sec-Fetch-Dest:document" -H "Connection:close"```

This string can then be pasted as part of a command with tools using this syntax.

**Known supported tools:**

- cURL
- Gobuster
- Feroxbuster *
- Wfuzz
- ffuf

## Known Issues

- *Feroxbuster doesn't like `Accept` or `Accept-Language` headers for some reason, so they're not included in the copied output.
- *Feroxbuster will only accept the `User-Agent` header using `-a,` / `--user-agent`, so for now, personally, I'm just manually changing that `-H` to `-a` and removing the header name. I'll probably make some more options at some point that will make this easier.

## TODO:

- Make submenu with different formats like "--headers", "Without User-Agent" etc.

## Author

- n0kovo (GitHub: [n0kovo](https://github.com/n0kovo), Mastodon: [@n0kovo@infosec.exchange](https://infosec.exchange/@n0kovo))
