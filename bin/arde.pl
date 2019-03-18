#!/usr/bin/perl

use strict;
use warnings;
require './conv2arde.pl';

while (<>) {
	chomp;
	next if ($_ eq "");
	my $r = conv2arde(regularize($_));

	print "$_\n> $r\n";
}

exit 0;
