RUSTPATH=${1}

mkdir res/

# benching mcfg 
cd $RUSTPATH

for i in 1 2 3 4 5 6 7 8 9 10
do
	target/debug/rustomata mcfg parse $OLDPWD/corp/pmcfg-10.gr < $OLDPWD/corp/pmcfg-10.txt
done