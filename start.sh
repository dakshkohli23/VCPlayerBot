echo "Starting...."
if [ -z $BRANCH ]
then
  echo "Cloning main branch...."
  else
  echo "Cloning $BRANCH branch...."
fi
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py
