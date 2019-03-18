#!/usr/bin/perl

use strict;
use warnings;

my $scripturl = "knp.cgi";

my %knp_opt = (
	""         => 0,
	"-simple"  => 1,
	"-tab"     => 2,
);

my %p = parseform(querystring());
my $sentence = $p{sentence};
my $knp_option = $p{knp_option};
my $result = knp($sentence, $knp_option);

screen($scripturl, $sentence, $knp_option, $result);

exit 0;

sub screen
{
	my $scripturl = shift;
	my $sentence = shift;
	my $knp_option = shift;
	my $result = shift;
	my @selected = ( "", "", "" );

	$result = boxdrawings($result);
	$selected[$knp_opt{$knp_option}] = "selected";

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
<h1>JUMAN+KNP構文解析デモ</h1>

<p><a href="http://nlp.ist.i.kyoto-u.ac.jp/?KNP">KNP本家サイト</a></p>

<form action="$scripturl" method="POST">
  <p> <input name="sentence" size="80" value="$sentence"> </p>
  <p> 
  <select name="knp_option">
    <option $selected[0] value="">なし</option>
    <option $selected[1] value="-simple">simple</option>
    <option $selected[2] value="-tab">tab</option>
  </select>
  <input type="submit" name="button" value="解析">
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

sub knp
{
	my $s = shift;
	my $o = shift;

	return if ($s eq "");
	$s = regularize($s);
	my $cmd = sprintf("echo '%s' | juman | knp %s", $s, $o);
	return `$cmd`;
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

sub regularize
{
	my $s = shift;

	$s =~ s/a/ａ/g; $s =~ s/b/ｂ/g; $s =~ s/c/ｃ/g; $s =~ s/d/ｄ/g;
	$s =~ s/e/ｅ/g; $s =~ s/f/ｆ/g; $s =~ s/g/ｇ/g; $s =~ s/h/ｈ/g;
	$s =~ s/i/ｉ/g; $s =~ s/j/ｊ/g; $s =~ s/k/ｋ/g; $s =~ s/l/ｌ/g;
	$s =~ s/m/ｍ/g; $s =~ s/n/ｎ/g; $s =~ s/o/ｏ/g; $s =~ s/p/ｐ/g;
	$s =~ s/q/ｑ/g; $s =~ s/r/ｒ/g; $s =~ s/s/ｓ/g; $s =~ s/t/ｔ/g;
	$s =~ s/u/ｕ/g; $s =~ s/v/ｖ/g; $s =~ s/w/ｗ/g; $s =~ s/x/ｘ/g;
	$s =~ s/y/ｙ/g; $s =~ s/z/ｚ/g;
	$s =~ s/a/ａ/g;
	$s =~ s/A/Ａ/g; $s =~ s/B/Ｂ/g; $s =~ s/C/Ｃ/g; $s =~ s/D/Ｄ/g;
	$s =~ s/E/Ｅ/g; $s =~ s/F/Ｆ/g; $s =~ s/G/Ｇ/g; $s =~ s/H/Ｈ/g;
	$s =~ s/I/Ｉ/g; $s =~ s/J/Ｊ/g; $s =~ s/K/Ｋ/g; $s =~ s/L/Ｌ/g;
	$s =~ s/M/Ｍ/g; $s =~ s/N/Ｎ/g; $s =~ s/O/Ｏ/g; $s =~ s/P/Ｐ/g;
	$s =~ s/Q/Ｑ/g; $s =~ s/R/Ｒ/g; $s =~ s/S/Ｓ/g; $s =~ s/T/Ｔ/g;
	$s =~ s/U/Ｕ/g; $s =~ s/V/Ｖ/g; $s =~ s/W/Ｗ/g; $s =~ s/X/Ｘ/g;
	$s =~ s/Y/Ｙ/g; $s =~ s/Z/Ｚ/g;
	$s =~ s/0/０/g; $s =~ s/1/１/g; $s =~ s/2/２/g; $s =~ s/3/３/g;
	$s =~ s/4/４/g; $s =~ s/5/５/g; $s =~ s/6/６/g; $s =~ s/7/７/g;
	$s =~ s/8/８/g; $s =~ s/9/９/g;
	$s =~ s/ /　/g;  $s =~ s/!/！/g;  $s =~ s/\"/”/g; $s =~ s/#/＃/g;
	$s =~ s/\$/＄/g; $s =~ s/\%/％/g; $s =~ s/\&/＆/g; $s =~ s/\'/’/g;
	$s =~ s/\(/（/g; $s =~ s/\)/）/g; $s =~ s/\*/＊/g; $s =~ s/\+/＋/g;
	$s =~ s/,/，/g;  $s =~ s/-/－/g;  $s =~ s/\./．/g; $s =~ s/\//／/g;
	$s =~ s/:/：/g;  $s =~ s/;/；/g;  $s =~ s/\</＜/g; $s =~ s/=/＝/g;
	$s =~ s/\>/＞/g; $s =~ s/\?/？/g; $s =~ s/\[/［/g; $s =~ s/\\/￥/g;
	$s =~ s/\]/］/g; $s =~ s/\^/＾/g; $s =~ s/_/＿/g;  $s =~ s/\`/‘/g;
	$s =~ s/{/｛/g;  $s =~ s/\|/｜/g; $s =~ s/}/｝/g;  $s =~ s/~/～/g;
	return $s;
}

sub boxdrawings
{
	my $s = shift;

	$s =~ s/\</&lt;/g;
	$s =~ s/\>/&gt;/g;
	$s =~ s/─/-/g;
	$s =~ s/┐/+/g;
	$s =~ s/┤/+/g;
	return $s;
}
