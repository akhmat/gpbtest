#use strict;
use DBI ;

my $user_name = "gpb";
my $password = "gbptest";
my $dbh = DBI->connect ("DBI:Pg:dbname=gpbtest;host=localhost",$user_name,$password );
$dbh -> do ( "SET NAMES 'utf8'" ) ;

my $sql = "insert into message (created, id, int_id, str, status) values (?,?,?,?,?)" ;
my $sth_insmes = $dbh -> prepare($sql) ;
my $sql = "insert into log (created, int_id, str, address) values (?,?,?,?)" ;
my $sth_inslog = $dbh -> prepare($sql) ;

open(F, "$ARGV[0]") or die "cant open $ARGV[0]" ;
my $id = "";
my $address = "" ;
my $cc = 0 ;
while(<F>){
	chomp;
	my @tmp = split(/ /,$_);
	if (@tmp >3){
		my $dt = "$tmp[0] $tmp[1]" ; 
		my $int_id = $tmp[2] ;
		my $flag = $tmp[3] ;
		my $address = $tmp[4] ;
		my $rest = join(' ',  @tmp[4..$#tmp]) ;
#		($address) = $rest =~ /([a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9._-]*\.[a-zA-Z]{2,})/ ;
		print "rest = $rest\n" ;
		$address =~ s/[:<>]//g;#убираем в позиции адреса лишнии символы
		if ( $flag eq "<="){
			($id) = $rest =~ /id=(\S+)/ ;
			if ($id){
				$sth_insmes -> execute($dt,$id, $int_id, "$int_id $flag $rest", 1) ;
			}
		}else{
			$sth_inslog -> execute($dt, $int_id,"$int_id $flag $rest", $address );
		}
		
	}
	$cc++;
#	last if ($cc>10);
}
close(F) ;

