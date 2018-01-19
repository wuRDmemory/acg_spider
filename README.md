Python入门：scrapy spider

最近想系统学习一下Python，然后就想用爬虫作为入门的训练，学习了一段时间的scrapy，然后结合这知乎上的例子进行了改进编写，最终有了初版程序，感谢知乎大神的无私分享。

知乎链接：https://www.zhihu.com/question/27621722/answer/269085034

然后该程序是在Python3下的Scrapy上运行，需要事先进行安装，过程中我也遇到了很多问题，写了一个总结性的博客，链接http://blog.csdn.net/wubaobao1993/article/details/79089552，希望可以帮助一些小伙伴。当然，Python2也是可以运行的，但是要改变一些语句，主要是urllib，在Python2中并没有吧模块分的这么清楚，具体的改进可以看这个博客：http://blog.csdn.net/whatday/article/details/54710403

具体的改进：
1.知乎的程序是抓取acg网站中的动漫版块，程序改为了抓取所有的版块;
2.知乎的程序是采用函数的形式对图像进行的保存，本程序中借助了scrapy的Item和Pipeline模块，感觉十分好用;
