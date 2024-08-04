osascript -e 'tell app "Terminal"
    do script "minio server miniodata"
end tell'

osascript -e 'tell app "Terminal"
    do script "./Documents/faks/vybe/elasticsearch/bin/elasticsearch"
end tell'

osascript -e 'tell app "Terminal"
    do script "./Documents/faks/vybe/kibana/bin/kibana"
end tell'
