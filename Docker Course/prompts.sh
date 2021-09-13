#To join from other nodes into a swarm
docker swarm join --token SWMTKN-1-1wk9vighiih32oxiwz2t91avdvfja1zm2xfv516te9otw9kl7a-asm60cc12hjv5vn9lusxvl5le 192.168.0.13:2377

#To deploy NGINX service:
docker service create --detach=true --name nginx1 --publish 80:80  --mount source=/etc/hostname,target=/usr/share/nginx/html/index.html,type=bind,ro nginx:1.12 pgqdxr41dpy8qwkn6qm7vke0q