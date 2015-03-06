# small_mathjax

small_mathjax is a Python script for reducing the size of [MathJax](http://mathjax.org) base on [the wiki article](https://github.com/mathjax/MathJax-docs/wiki/Guide%3A-reducing-size-of-a-mathjax-installation). If you want to serve mathjax on your website, or integrate it with mobile apps, you can use the tool to get a much smaller size of code.

## usage


- You can download the code, it depends on nothing but Python itself. Check and modify the sample.conf based on your own requirements.
- Download the MathJax release package and uncompress it into a directory, say MathJax-2.5.1.
- Test it with a dryrun, check the output log.
```
python small_mathjax.py -c sample.conf MathJax-2.5.1
```
- Now, let the MathJax become small, (with -e option).
```
python small_mathjax.py -c smaple.conf -e MathJax.2.5.1
```

