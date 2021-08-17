# Developer Instructions
These instructions should help developers understand how to connect to the kafka ressources within the cluster.

## Kafka specific vocabulary
First of all a basic rundown of important Kafka language:
<ul>

<li>
Consumer:
</li>

Some Pod that subscribes to a certain kafka topic and reads all data written into that topic

<li>
Producer: 
</li>

Some Pod that publishes data into a certain kafka topic. It streams data into the topic.

<li>
Topic: 
</li>

Pool of messages that have a common purpose. For example for new loans that users make you would have a topic ("loan-book-topic") and for books that are added to the library you would have another topic ("book-stream-topic"). The reason is that some script might be interested in new book loans but it doesn't care about new books that are added to the library. Another script might be interested in new books in the library but doesn't care about any loans.

<li>
Bootstrap server:
</li>
Is a Kafka Server that can be contacted by producers and consumers to get information about the kafka cluster. It is necessary to give this server to producers and consumers, so that they know how and where to stream their data to and from.

</ul>



## How to connect to Kafka
To use kafka in python you need ```kafka-python```, here is the [official documentation](https://kafka-python.readthedocs.io/en/master/usage.html). Write kafka-python into the ```requirements.txt``` of the respective folder, it will be automatically installed by the container (definied in the Dockerfile of that folder). To use kafka in the python file you don't need to write ~~```import kafka-python```~~ instead you use this line:

```python
import kafka
```

[Here](https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1) are instructions on how to set up kafka in an example application.

<br>

To connect to kafka you need to specify the kafka bootstrap server.

This is the **bootstrap server for consumers**:
```
kafka-release.legerible-kafka.svc.cluster.local:9092
```

This is the **bootstrap server for producers**:
```
kafka-release-0.kafka-release-headless.legerible-kafka.svc.cluster.local:9092
```

<br>

It is also necessary to specify a topic.
I suggest we use two different topics:

<ol>
<li><b>loan-book-topic</b></li>
This topic will contain all data streams that are related to new loans that users make.
The streamed data is in json format and the json has two key value pairs: user_id (int) and book_id (int)

Some json example:

{\
    "user_id": 1,\
    "book_id": 5\
}

<li><b>book-stream-topic</b></li>
This topic will contain all data streams that are related to new books that are available in the library. Technically they are randomly generated ISBNs but we suppose that the data is streamed from the library server, because the new books were scanned in the library.

The streamed data is again in json format and will only contain the isbn of the book. Key value pairs: isbn (int)

Json example:

{\
"isbn": 0123456789\
}
</ol>