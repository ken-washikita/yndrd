#!/usr/bin/perl

use strict;
use warnings;
use KNP::Simple -Option => "-tab";
use KNP::Result;

sub conv2arde
{
	my $s = shift;
	my $r = "";

	my $result = knp($s);

	my @o;

	my $nTheme = -1;
	my $nMain = -1;
	my $n = 0;
	foreach my $bnst ($result->bnst) {
		if ($bnst->fstring =~ /<提題>/) {
			$nTheme = $n;
		}
		if ($bnst->fstring =~ /<SM-主体>/) {
			$nMain = $n;
		}
		if ($bnst->fstring =~ /<提題受:/) {
			$nTheme = $nMain if ($nTheme == -1 && $nMain != -1);
			if ($nTheme != -1) {
				splice(@o, $nTheme + 1, 0, $n);
				next;
			}
		}
		push(@o, $n);
		$n++;
	}

	my $fPeriod = 0;
	my $fQuestion = 0;
	foreach my $i (0 .. $#o) {
		my $fCase = 0;
		my $bnst = ($result->bnst)[$o[$i]];
		if ($bnst->fstring =~ /<係:ノ格>/) {
			$fCase = 1;
		}
		foreach my $m ($bnst->mrph_list) {
			my ($t, $u) = split(/ /, $m->spec, 2);
			$fCase = 1 if ($t eq "だけ");
			if ($t eq "。") { $fPeriod = 1; next; }
			if ($t eq "？") { $fQuestion = 1; next; }
			next if ($u =~ / 助詞 / && !$fCase);
			next if ($u =~ / 判定詞 /);
			$r .= $t;
		}
	}
	$r .= "。" if ($fPeriod);
	$r .= "？" if ($fQuestion);
	return $r;
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

1;
