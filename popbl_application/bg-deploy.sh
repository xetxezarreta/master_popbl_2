# get 'app' label value from the service selector (django-blue or django-green)
res=$(kubectl get svc django -o custom-columns="SELECTOR:.spec.selector.app" | tail -n 1); 

if [ $res == "django-blue" ]; then 
    kubectl set image deploy/django-green web=$IMAGE_RELEASE_PROD; 
    kubectl scale --replicas=2 deploy.apps/django-green; 
    kubectl rollout status deployment django-green -w ; 
    dcolor='kubectl patch service django -p '"'"'{"spec":{"selector":{"app": "django-green", "deployment": "green" }}}'"'"''; 
    kubectl scale --replicas=0 deploy.apps/django-blue ; 
else 
    kubectl set image deploy/django-blue web=$IMAGE_RELEASE_PROD; 
    kubectl scale --replicas=2 deploy.apps/django-blue;
    kubectl rollout status deployment django-blue -w; 
    dcolor='kubectl patch service django -p '"'"'{"spec":{"selector":{"app": "django-blue", "deployment": "blue" }}}'"'"''; 
    kubectl scale --replicas=0 deploy.apps/django-green;

