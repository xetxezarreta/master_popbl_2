wget https://prod.itapp.eus --no-check-certificate
xmllint --html --xpath '//div[@class="footer"]' index.html > tmp
stringarray=($(cat tmp))
res1=`eval echo ${stringarray[2]}`

xmllint --html --xpath '//div[@class="footer"]' web/app/app/templates/index.html > tmp
stringarray=($(cat tmp))
res2=`eval echo ${stringarray[2]}`

echo $res1
echo $res2

if [ $res1 == $res2 ]
then
  echo "Version match"
  exit 0
else
  echo "Version missmatch"
  exit -1
fi
