---
title: "ffmpeg on mobile"
---

tldr: ffmpeg + Termux + LLM  
So, I don't really know why it didn't came to me earlier, but ffmpeg can and should be used on mobile as well.  
I've found myself needing a media conversion/transcoding/editing tool more than once in this life.

And via [Termux](https://termux.dev/en/), all of the capabilities of the amazing [ffmpeg](https://www.ffmpeg.org/documentation.html) suite are just some commands away..

```
pkg update 
pkg upgrade
pkg install ffmpeg

# check the version with 
ffmpeg -version 

# enable storage access for termux 
termux-setup-storage
```

Additionally, I have a gemini/claude interface in a background tab, just in case I need some help. And it works like a charm.
