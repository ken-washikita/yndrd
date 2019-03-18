#!/usr/bin/perl

use strict;
use warnings;
require './conv2arde.pl';

my $scripturl = "index.cgi";

my $result = "";

my %p = parseform(querystring());
my $sentence = $p{sentence};
if ($sentence ne "") {
	$result = conv2arde(regularize($sentence));
}

screen($scripturl, $sentence, $result);

exit 0;

sub screen
{
	my $scripturl = shift;
	my $sentence = shift;
	my $result = shift;

	print <<EOL;
Content-type: text/html

<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style type="text/css">
<!--
pre { font-family: monospace, sans-serif; }
-->
</style>
</head>
<body>
<h1>きみしてるだけ言葉遊び</h1>

<p><a href="http://nlp.ist.i.kyoto-u.ac.jp/?KNP">KNP本家サイト</a></p>

<form action="$scripturl" method="POST">
  <p> <input name="sentence" size="80" value="$sentence"> </p>
  <p> 
  <input type="submit" name="button" value="変換">
  <input type="reset">
  </p>
</form>
<pre>
$result
</pre>
</body>
</html>
EOL
}

sub querystring
{
	my $s;

	if ($ENV{REQUEST_METHOD} eq "POST") {
		read(STDIN, $s, $ENV{CONTENT_LENGTH});
	} else {
		$s = $ENV{QUERY_STRING};
	}
	return $s;
}

sub parseform
{
	my $s = shift;
	my %p;

	foreach my $t (split(/&/, $s)) {
		my ($k, $v) = split(/=/, $t);
		$v =~ tr/+/ /;
		$v =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		$p{$k} = $v;
	}
	return %p;
}
