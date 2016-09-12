sudo echo "Welcome"
sudo socat -d -d pty,raw,echo=0,link=/dev/prosper_prospekt,user=jo pty,raw,echo=0,link=/dev/prospekt,user=jo & 
sudo socat -d -d pty,raw,echo=0,link=/dev/prosper_pump,user=jo pty,raw,echo=0,link=/dev/pump,user=jo &
sleep 1
python ./pump_simulator.py &
python ./simulator.py 

