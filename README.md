# Bio101 - UESTC-SOFTWARE

<h1>Quick Start</h1>
<p>Just visit our website:<br>
<a href="http://bio101.uestc.edu.cn/transform/">bio101.uestc.edu.cn/transform</a><br>
and enjoy it!
<p>

<h1>Overview</h1>
<p> <strong>Bio101</strong>:DNA Information Storage System is such a bridge between bits and nucleotides, i.e. between the current information techology (IT) world and the future biotechnology (BT) computing world, and it is designed for the information transformation between computer files and DNA sequences.It also provides editing function using the CRISPR/CAS9 system.</p>
<h3>Workflow：Archival mode </h3>

<img src="http://bio101.uestc.edu.cn/static/images/about_5.png" >
<p>Five steps in our workflow:
<ol>
<li>Compress - bzip2</li>
<li>Encrypt - isaac</li>
<li>Bit2Nt </li>
<li>Fragment and Add Index</li>
<li>Validation</li>
</ol>
<p>
In biotechnology, result is synthesized into DNA substcance for information storage.To extract this information, DNA need be sequenced, and decoded.
As we can see here, decoding is the reverse of encoding.There same four steps:
</p>
<ol>
<li>Sequncing</li>
<li>Decode into long sequence</li>
<li>Nt2Bit</li>
<li>Decript</li>
<li>Decompress</li>
</ol>
<img src="http://2016.igem.org/wiki/images/9/96/Uestc_software-modeling_table2.png" >
<p style="fontsize:small;text-align:center;">Bit Nt translation table</p>
</p>
<h3>Workflow：Editable mode</h3>
<img src="http://2016.igem.org/wiki/images/2/27/Uestc_software-011.jpg">
<p>To support DNA edit, we split original file into small segements before scrambling,and indepent segments can be decode and edit directly.</p>
<p>Editing results will be displayed as text or SBOL file.</p>

<p>Choosing 'Editable mode',users can edit any single DNA segment,and change the content of it.This needs help from Cas9 to destroy original DNA substance,so we also provide  a sgRNA for target.</p>

<h3>Directory Structure</h3>
<pre>
<code>
.
├── Bio101
│   ├── settings.py
│   ├── urls.py
│   ├── urls.py.bk
│   └── wsgi.py
├── Uestc_software-logo_40px.png
├── Uestc_software-logo_54px.png
├── db.sqlite3
├── manage.py
├── run
├── static
│   ├── css
│   │   ├── AjaxLoader.gif
│   │   ├── OpenSans.css
│   │   ├── bootstrapTheme.css
│   │   ├── custom.css
│   │   ├── grabbing.png
│   │   ├── owl.carousel.css
│   │   └── owl.theme.css
│   └── js
│       ├── application.js
│       ├── bootstrap-collapse.js
│       ├── bootstrap-tab.js
│       ├── bootstrap-transition.js
│       ├── jquery-1.9.1.min.js
│       └── owl.carousel.js
├── templates
│   └── transform
│       ├── about.html
│       ├── base.html
│       ├── decode.html
│       ├── edit.html
│       ├── encode.html
│       └── index.html
├── transform
│   ├── admin.py
│   ├── apps.py
│   ├── convert
│   │   ├── __init__.py
│   │   ├── bit2nt
│   │   ├── blastn -> blastn-linux_x64-2.5.0
│   │   ├── blastn-2.5.0
│   │   ├── blastn-linux_x64-2.5.0
│   │   ├── c_source
│   │   │   ├── bit2nt
│   │   │   ├── bit2nt.c
│   │   │   ├── isaac64
│   │   │   ├── isaac64.c
│   │   │   ├── isaac64.h
│   │   │   ├── nt2bit
│   │   │   ├── nt2bit.c
│   │   │   └── standard.h
│   │   ├── convert.py
│   │   ├── decode.py
│   │   ├── encode.py
│   │   ├── isaac64
│   │   └── nt2bit
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
</code>
</pre>
<h1>Dependences</h1>
<h2>Algorithm and Utilities</h2>
<ul>
<li>ISAAC -<a href="http://burtleburtle.net/bob/rand/isaac.html">http://burtleburtle.net/bob/rand/isaac.html</a></li>
<li>Bzip2 -<a href="http://www.bzip.org">http://www.bzip.org</a></li>
<li>Tar - <a href="http://linuxcommand.org/man_pages/tar1.html">http://linuxcommand.org/man_pages/tar1.html</a></li>
</ul>

<h2>Front End</h2>
<ul>
<li>OWL Carousel - <a href="http://owlgraphic.com/owlcarousel">http://owlgraphic.com/owlcarousel</a></li>
<li>Boostrap - <a href="http://getbootstrap.com/">http://getbootstrap.com/</a></li>
<li>jQuery - <a href="https://jquery.com/">https://jquery.com/</a></li>
</ul>

<h2>Back End</h2>
<ul>
<li>Pyhton 2.7</li>
<li>Django 1.8.9 <a href="https://www.djangoproject.com">https://www.djangoproject.com</a></li>
</ul>
<h1>Installation</h1>
Make sure that there is python-2.7 on your machine.
And if you want to run the server on your computer, you need Django-1.8.9.


Enter the location of downloaded file, like:
<pre>
<code>
cd git/UESTC-Software-2016-master/Bio101_v4
</code>
</pre>
Run server in Django.
<pre>
<code>
./run
</code>
</pre>

You wiil see results like:
<pre>
<code>
System check identified no issues (0 silenced).
October 20, 2016 - 02:53:43
Django version 1.8, using settings 'Bio101.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
</code>
</pre>
<p>If you are using OSX,you can recompile five .c file in Conver Folder.(Our app is running in service.),by:
<pre>
<code>
cd transform/convert
gcc c_source/bt2nt.c -O2 -o bit2nt
gcc c_source/isaac.c -O2 -o isaac
gcc c_source/nt2bt.c -O2 -o nt2bt
gcc c_source/isnt2bt  -O2 -o isnt2bt
gcc c_source/isnt2bt  -O2 -o isnt2bt
</code>
</pre>
When you finish this, you can just run  file "RUN" by:</p>
<pre>
<code>
./run
</code>
</pre>
   <p> Visit <a href="http://127.0.0.1:8000/transform/">http://127.0.0.1:8000/transform/</a>,and you can enjoy our software.</p>
   <P>We have not run or tested our project on Windows, so we don't know the Dependences in it. </P>
<h1> Documentation</h1> 
<p>Please visit our online document page: <a href="http://2016.igem.org/Team:UESTC-software/Document" target="_blank">Document in Wiki</a>
<h1>About</h1>
<p>Developed by UESTC-SOFTWARE</p>

