
![[Pasted image 20251104112000.png]]

In this ctf we are given a log data and when we open it we a large large amounts of strings encoded in base64 and after we decode it we see that its an image and it contains something encoded in hex and when we decode the hex we get the flag



![[Pasted image 20251104112225.png]]


![[Pasted image 20251104112138.png]]


```bash
fahad@Workstation:~/Downloads$ echo "7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F62653836303237397D" | xxd -r -p

picoCTF{forensics_analysis_is_amazing_be860279}
```