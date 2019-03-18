#!/usr/bin/perl

use strict;
use warnings;
use KNP::Simple -Option => "-tab";
use KNP::Result;

my $scripturl = "index.cgi";

my %knp_opt = (
	""         => 0,
	"-simple"  => 1,
	"-tab"     => 2,
);

my %p = parseform(querystring());
my $sentence = $p{sentence};
my $knp_option = $p{knp_option};
my $result = conv2arde($sentence);

screen($scripturl, $sentence, $knp_option, $result);

exit 0;

sub screen
{
	my $scripturl = shift;
	my $sentence = shift;
	my $knp_option = shift;
	my $result = shift;
	my @selected = ( "", "", "" );

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

sub conv2arde
{
	my ($s) = shift;
	my $r = "";

	my $result = knp($s);

	my @o;

	my $nTheme = -1;
	my $n = 0;
	foreach my $bnst ($result->bnst) {
		if ($bnst->fstring =~ /<提題>/) {
			$nTheme = $n;
		}
		if ($bnst->fstring =~ /<提題受:/ && $nTheme >= 0) {
			splice(@o, $nTheme + 1, 0, $n);
		} else {
			push(@o, $n);
		}
		$n++;
	}

	foreach my $i (0 .. $#o) {
		my $fCase = 0;
		my $fPeriod = 0;
		my $bnst = ($result->bnst)[$o[$i]];
		if ($bnst->fstring =~ /<係:ノ格>/) {
			$fCase = 1;
		}
		foreach my $m ($bnst->mrph_list) {
			my ($t, $u) = split(/ /, $m->spec, 2);
			$fCase = 1 if ($t eq "だけ");
			if ($t eq "。") {
				$fPeriod = 1; next;
			}
			next if ($u =~ / 助詞 / && !$fCase);
			next if ($u =~ / 判定詞 /);
			$r .= $t;
		}
	}
	$r .= "。" if ($fPeriod);
	return $r;
}
