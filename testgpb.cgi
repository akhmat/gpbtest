#!C:/Perl/perl/bin/perl.exe
use strict;
use warnings;
use CGI;
use DBI ;

my $q = CGI->new;
my $email = $q->param('email') || '';
my $safe_email = $q->escapeHTML($email);
print $q->header(-type => 'text/html', -charset => 'UTF-8');

print <<HTML;
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Тестовый CGI скрипт</title>
    <style>
        pre { background: #f4f4f4; padding: 10px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h2>Введите email адрес получателя</h2>
    <form method="GET" action="">
        <input type="text" name="email" value="" placeholder="почта..." autofocus>
        <input type="submit" value="Отправить">
    </form>
HTML

if ($safe_email) {

my $user_name = "gpb";
my $password = "gbptest";
my $dbh = DBI->connect ("DBI:Pg:dbname=gpbtest;host=localhost",$user_name,$password );
$dbh -> do ( "SET NAMES 'utf8'" ) ;
#my $sql = "select created, str from ((select created, str, int_id from message where address like '\%$safe_email\%' union select created,str, int_id from log where address like '\%$safe_email\%'))z order by int_id limit 101";
my $sql = q{
    SELECT created, str 
    FROM (
        (SELECT created, str, int_id FROM message WHERE str LIKE ? 
         UNION 
         SELECT created, str, int_id FROM log WHERE address LIKE ?)
    ) AS z 
    ORDER BY int_id 
    LIMIT 101
};
$email =~ s/([_%])/\\$1/g; #экранируем плейсхолдеры в LIKE
my $param = '%' . $email . '%' ;
my $sth = $dbh -> prepare($sql) ;
$sth -> execute($param,$param);
my $created = "";
my $str = "" ;
print "<pre>" ;
my $cc = 0 ;
while(($created,$str) = $sth->fetchrow){
	print $q->escapeHTML("$created\t$str\n") ;
	$cc++;
	if ($cc>=100){
		print "!!!Больше 100 записей в результате!!!\n" ;
		last;
	}
}
print"</pre>"
}

print <<HTML;
</body>
</html>
HTML