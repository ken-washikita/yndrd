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
	$s = shellsafe($s);
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

sub shellsafe
{
	my $s = shift;

	$s =~ s/ /　/g;     # KNP requirement
	$s =~ s/\</＜/g;
	$s =~ s/\>/＞/g;
	$s =~ s/\&/＆/g;
	$s =~ s/\|/｜/g;
	$s =~ s/\'/’/g;
	$s =~ s/\"/”/g;
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
