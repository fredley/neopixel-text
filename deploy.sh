PI=zero

scp *.py $PI:neopixel/
scp *.ttf $PI:neopixel/
scp -r templates $PI:neopixel/
scp uwsgi.ini $PI:neopixel/
scp pixel.service $PI:neopixel/

ssh $PI -t 'sudo cp neopixel/pixel.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl restart pixel'
