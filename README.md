# Bio101 - UESTC-SOFTWARE

<h1>Quick Start</h1>
<p>Just visit our website:<br>
<a href="bio101.uestc.edu.cn/transform">bio101.uestc.edu.cn/transform</a><br>
and enjoy it!
<p>

<h1>Overview</h1>
<p> <strong>Bio101</strong>:DNA Information Storage System is such a bridge between bits and nucleotids, i.e. between the current information techology (IT) world and the future biotechnology (BT) computing world, and it is designed for the information transformation between computer files and DNA sequences.It also provides edit function embracing CAS-9'knockout feature.</p>
<h3>Workflow</h3>

<img src="http://bio101.uestc.edu.cn/static/images/about_5.png" >
<p>Four steps in our workflow:
<ol>
<li>Compress - bzip2</li>
<li>Encrypt - isaac</li>
<li>Bit2Nt </li>
<li>Fragment and Add Index</li>
</ol>
<p>
In biotechnology, result is synthesized into DNA substcance for information storage.To extract this information, DNA need be sequenced, and decoded.
As we can see here, decoding is the reverse of encoding.There same four steps:
</p>
<ol>
<li>Decode into long sequence</li>
<li>Nt2Bit</li>
<li>Decript</li>
<li>Decompress</li>
</ol>
<img src="http://2016.igem.org/wiki/images/9/96/Uestc_software-modeling_table2.png" >
<p style="fontsize:small;text-align:center;">Bit Nt translation table</p>
</p>



<h3>Directory Structure</h3>
<pre>
<code>
.
├── Bio101
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── media
│   ├── download
│   │   ├── display-original.bz2
│   │   └── display-original_DC0Nbxi.bz2
│   └── upload
│       ├── display-original
│       └── display-original_DC0Nbxi
├── ncbi-blast-2.5.0+-x64-macosx.tar.gz
├── run
├── static
│   ├── css
│   │   ├── AjaxLoader.gif
│   │   ├── OpenSans.css
│   │   ├── bootstrapTheme.css
│   │   ├── custom.css
│   │   ├── owl.carousel.css
│   │   └── owl.theme.css
│   ├── images
│   │   └── favicon.ico
│   └── js
│       ├── application.js
│       ├── bootstrap-collapse.js
│       ├── bootstrap-tab.js
│       ├── bootstrap-transition.js
│       ├── jquery-1.9.1.min.js
│       └── owl.carousel.js
├── templates
│   └── transform
│       ├── about.html
│       ├── base.html
│       ├── decode.html
│       ├── encode.html
│       └── index.html
└── transform
    ├── admin.py
    ├── apps.py
    ├── convert
    │   ├── __init__.py
    │   ├── bit2nt
    │   ├── blastn -> blastn-linux_x64-2.5.0
    │   ├── blastn-2.5.0
    │   ├── blastn-linux_x64-2.5.0
    │   ├── c_source
    │   │   ├── bit2nt
    │   │   ├── bit2nt.c
    │   │   ├── isaac64
    │   │   ├── isaac64.c
    │   │   ├── isaac64.h
    │   │   ├── nt2bit
    │   │   ├── nt2bit.c
    │   │   └── standard.h
    │   ├── convert.py
    │   ├── database
    │   │   ├── BIOBRICKS.nhr
    │   │   ├── BIOBRICKS.nin
    │   │   └── BIOBRICKS.nsq
    │   ├── decode.py
    │   ├── encode.py
    │   ├── isaac64
    │   └── nt2bit
    ├── forms.py
    ├── models.py
    ├── urls.py
    └── views.py
</code>
</pre>
<h1>Dependences</h1>
<h2>Algorithm</h2>
<ul>
<li>ISAAC -<a href="http://burtleburtle.net/bob/rand/isaac.html">http://burtleburtle.net/bob/rand/isaac.html</a></li>
<li>Zlip2 -<a href="http://www.bzip.org">http://www.bzip.org</a></li>
<li>Fuzzy matching</li>
</ul>

<h2>Front End</h2>
<ul>
<li>Boostrap - <a href="http://getbootstrap.com/">http://getbootstrap.com/</a></li>
<li>OWL Carousel - <a href="http://owlgraphic.com/owlcarousel">http://owlgraphic.com/owlcarousel</a></li>
<li>jQuery - <a href="https://jquery.com/">https://jquery.com/</a></li>
</ul>

<h2>Back End</h2>
<ul>
<li>Pyhton 2.7</li>
<li>Django 1.8 - <a href="https://www.djangoproject.com">https://www.djangoproject.com</a></li>
</ul>
<h1> Documentation</h1> 
<p>Please visit our online help page:<a href="http://2016.igem.org/Team:UESTC-software/Document">Document in Wiki</a>
<h1>About</h1>
<p>Developed by UESTC-SOFTWARE</p>

