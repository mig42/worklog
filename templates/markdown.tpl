<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"$if(lang)$ lang="$lang$" xml:lang="$lang$"$endif$>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta http-equiv="Content-Style-Type" content="text/css" />
  <meta name="generator" content="pandoc" />
$for(author-meta)$
  <meta name="author" content="$author-meta$" />
$endfor$
$if(date-meta)$
  <meta name="date" content="$date-meta$" />
$endif$
  <link rel="icon" type="image/x-icon" href="/img/favicon.ico" />
  <link href='http://fonts.googleapis.com/css?family=Droid+Sans+Mono' rel='stylesheet' type='text/css'>
  <title>$if(title-prefix)$$title-prefix$ - $endif$$pagetitle$</title>
  <style type="text/css">code{white-space: pre;}</style>
$if(quotes)$
  <style type="text/css">q { quotes: "“" "”" "‘" "’"; }</style>
$endif$
$if(highlighting-css)$
  <style type="text/css">
$highlighting-css$
  </style>
$endif$
$for(css)$
  <link rel="stylesheet" href="$css$" $if(html5)$$else$type="text/css" $endif$/>
$endfor$
$if(math)$
  $math$
$endif$
$for(header-includes)$
  $header-includes$
$endfor$
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
  <script src="/js/core.js"></script>
</head>
<body class="markdown-body">
$for(include-before)$
$include-before$
$endfor$
$if(title)$
<div id="$idprefix$header">
<h1 class="title">$title$</h1>
$if(subtitle)$
<h1 class="subtitle">$subtitle$</h1>
$endif$
$for(author)$
<h2 class="author">$author$</h2>
$endfor$
$if(date)$
<h3 class="date">$date$</h3>
$endif$
</div>
$endif$
<a href="#" class="scroll totop">Scroll</a>
<a href="#end" class="scroll tobottom">Scroll</a>
$if(toc)$
<div id="$idprefix$TOC">
$toc$
</div>
$endif$
$body$
$for(include-after)$
$include-after$
$endfor$
<a id="end" />
</body>
</html>
