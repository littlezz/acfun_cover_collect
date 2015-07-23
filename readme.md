This is a script that download the cover image of h.acfun.tv

直接下载图包
[images.zip](https://github.com/littlezz/acfun_cover_collect/releases/download/v1.2/images.zip)



Require
---------
- python3
- requests
- [fix_headers_parse](https://github.com/littlezz/fix-headers-parse)


Screen shot
-------------
result

![](/screenshot/ss1.png)



编码问题
----------
`encode('latin1').decode('utf8')` 这个做法是正确的。

requests最近的一次提交修正了这个问题
(https://github.com/kennethreitz/requests/pull/2655/commits)

然而现在的问题是， 某些情况下location中的url时不完整的， 特点是都已\x85结尾， 而且我花了一个下午成功重现过一次， 里面包含有两个`-`

现在的问题是， url缺失是requests的锅还是httplib的锅。

#### 2015年07月22日15:59:11
依赖fix_headers_parse (https://github.com/littlezz/fix-headers-parse), 编码问题得到了解决， 详细的细节也在那里进行了说明。



### Damn it! (好吧， 不是A岛的锅， 后面的东西留在这里当做是黑历史吧)

Firstly, i lost my chinese input method and my english is not pretty good, but i still want to  *fxck* the man who does not use 'utf8'!  
it waste me more than 4 hours to know the url is encoded by 'gbk' instead of 'utf8'! Damn it!  
At first, i can not acess the url, i guess that i do not have cookies or not set up the correct headers, then i try change the headers,but it doesn't work,
i always got the 404 error. It took me 1 hour to fight with the headers.  
Later, I realize that the url encoding is wrong! And then , i spent 3 hours to find out we should use 'gbk' and  how to turn to the correct url!
Damn it !  
But what really make me crazy is that some url still do not work!  
It cost me another 2 hours to find out some url is not encoded by 'gbk',just by the friendly utf8!!  
fxxx! !!!

there is a saying:

> One day i have a blade, die out the gbker!

why not use utf8?  
hy not use utf8?  
y not use utf8?  
not use utf8?  
ot use utf8?  
t use utf8?  
use utf8?  
se utf8?  
e utf8?  
utf8?  
tf8?  
f8?  
8?  
?  





### ~How to use~

just run and wish the man who use 'gbk' go hell


