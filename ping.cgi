#!/bin/sh -f

echo "Content-type: application/json"
echo ""

TIMESTAMP_MS=`date +"%s.%3N"`
TMP_FILENAME="/tmp/ping.sh-$TIMESTAMP_MS.tmp"

if ! [[ -e $TMP_FILENAME ]]; then
	echo "1" > $TMP_FILENAME
fi

if [ "$QUERY_STRING" = "" ] ; then

  echo "<h1>no query string? No host to check</h1>"

else 

	if [[ $QUERY_STRING =~ "&" ]]; then

		saveIFS=$IFS
		IFS='=&'
		parm=($QUERY_STRING)
		IFS=$saveIFS
	
		declare -A qs
		for ((i=0; i<${#parm[@]}; i+=2))
		do
			qs[${parm[i]}]=${parm[i+1]}
		done
	
		HOST=${qs["host"]}
		COUNT=${qs["count"]}

		## Initial Vars
		TRANSMITTED_P=""
		RECEIVED_P=""
		PACKET_LOSS_PERC=""
		PING_TIME_ms=""
		IP_ADDR=""

		CONTENT=`cat $TMP_FILENAME`
		COUNTED_CHARS=`echo $CONTENT |	wc -c`

		ping -c $COUNT $HOST > $TMP_FILENAME
		CONTENT_N=`cat $TMP_FILENAME`
		COUNTED_LINES=`cat $TMP_FILENAME |	wc -l`

		index=0
		while read -r line
		do
			
			if [[ $line =~ time=([0-9]+)\.([0-9]+) ]]; then
	
				array[index++]=${BASH_REMATCH[1]}"."${BASH_REMATCH[2]}
			else
	
				if [[ $line =~ "packets transmitted" ]]; then
					TRANSMITTED_P=`echo $line | awk -F ", " '{ print $1 }' | awk '{ print $1 }'`;
					#echo "trs<br>";
					RECEIVED_P=`echo $line | awk -F ", " '{ print $2 }' | awk '{ print $1 }'`;
					#echo "rcv<br>"
					
					PACKET_LOSS_PERC=`echo $line | awk -F ", " '{ print $3 }' | awk '{ print $1 }'`;
					#echo "perc<br>"
					
					PING_TIME_ms=`echo $line | awk -F ", " '{ print $4 }' | awk '{ print $2 }' | awk -F "ms" '{ print $1 }'`;
					# echo "time(ms)<br>"
	
				else 
					if [[ $line =~ ([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5]) ]]; then
						IP_ADDR=${BASH_REMATCH[1]}"."${BASH_REMATCH[2]}"."${BASH_REMATCH[3]}"."${BASH_REMATCH[4]}
					fi
				fi
	
	
			fi
		done < $TMP_FILENAME
	
		echo -n "{ "
	
		IP_ADDR="$(echo -e "${IP_ADDR}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
	
		echo -n "\"host\": \"$HOST\", "
		echo -n "\"addr_resolved\": \""$IP_ADDR"\", "
		echo -n "\"transmitted\": $TRANSMITTED_P, "
		echo -n "\"received\": $RECEIVED_P, "
		echo -n "\"loss_percent\": \"$PACKET_LOSS_PERC\", "
		echo -n "\"time_ms\": \"$PING_TIME_ms\", \"timings\": "
		echo -n "["
	
		COUNTED_ARR=${#array[@]}
		i_c=0
		for ms in "${array[@]}"
		do
			echo -n "\""$ms"\""
	
			if [[ $i_c -ne $((COUNTED_ARR-1)) ]]; then
				echo -n ", "
			fi
			i_c=$((i_c+1))
		done
		echo -n "]"
		echo -n ""
		echo -n " }"
	
		rm -rf $TMP_FILENAME >/dev/null


	else

		## Initial Vars
		TRANSMITTED_P=""
		RECEIVED_P=""
		PACKET_LOSS_PERC=""
		PING_TIME_ms=""
		IP_ADDR=""
	
		CONTENT=`cat $TMP_FILENAME`
		COUNTED_CHARS=`echo $CONTENT |	wc -c`

		ping -c 3 $QUERY_STRING > $TMP_FILENAME
		
		CONTENT_N=`cat $TMP_FILENAME`
		COUNTED_LINES=`cat $TMP_FILENAME |	wc -l`
		
		index=0
		while read -r line
		do
			
			if [[ $line =~ time=([0-9]+)\.([0-9]+) ]]; then
		
				array[index++]=${BASH_REMATCH[1]}"."${BASH_REMATCH[2]}
			else
		
				if [[ $line =~ "packets transmitted" ]]; then
					TRANSMITTED_P=`echo $line | awk -F ", " '{ print $1 }' | awk '{ print $1 }'`;
					#echo "trs<br>";
					RECEIVED_P=`echo $line | awk -F ", " '{ print $2 }' | awk '{ print $1 }'`;
					#echo "rcv<br>"
					
					PACKET_LOSS_PERC=`echo $line | awk -F ", " '{ print $3 }' | awk '{ print $1 }'`;
					#echo "perc<br>"
					
					PING_TIME_ms=`echo $line | awk -F ", " '{ print $4 }' | awk '{ print $2 }' | awk -F "ms" '{ print $1 }'`;
					# echo "time(ms)<br>"
		
				else 
					if [[ $line =~ ([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5]) ]]; then
						IP_ADDR=${BASH_REMATCH[1]}"."${BASH_REMATCH[2]}"."${BASH_REMATCH[3]}"."${BASH_REMATCH[4]}
					fi
				fi
		
		
			fi
		done < $TMP_FILENAME
		
		echo -n "{ "
		
		IP_ADDR="$(echo -e "${IP_ADDR}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
		
		echo -n "\"host\": \"$QUERY_STRING\", "
		echo -n "\"addr_resolved\": \""$IP_ADDR"\", "
		echo -n "\"transmitted\": $TRANSMITTED_P, "
		echo -n "\"received\": $RECEIVED_P, "
		echo -n "\"loss_percent\": \"$PACKET_LOSS_PERC\", "
		echo -n "\"time_ms\": \"$PING_TIME_ms\", \"timings\": "
		echo -n "["
		
		COUNTED_ARR=${#array[@]}
		i_c=0
		for ms in "${array[@]}"
		do
			echo -n "\""$ms"\""
		
			if [[ $i_c -ne $((COUNTED_ARR-1)) ]]; then
				echo -n ", "
			fi
			i_c=$((i_c+1))
		done
		echo -n "]"
		echo -n ""
		echo -n " }"
		
		rm -rf $TMP_FILENAME >/dev/null
		
		
	fi

fi

exit 0
