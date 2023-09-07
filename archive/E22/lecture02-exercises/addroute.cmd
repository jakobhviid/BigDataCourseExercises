@echo off
echo This function needs to be run with admin rights or it wont work!!!
echo adding route to default bridge
route /P add 172.200.0.0 MASK 255.255.0.0 10.0.75.2