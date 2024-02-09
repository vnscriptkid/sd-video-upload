const {PubSub} = require('@google-cloud/pubsub');
const pubSubClient = new PubSub();

// Replace 'your-topic-name' with your actual Pub/Sub topic name
const topicName = 'your-topic-name';
// Use an ordering key that makes sense for your application
const orderingKey = 'your-ordering-key';

async function publishOrderedMessages(topicName, orderingKey, messages) {
  const topic = pubSubClient.topic(topicName, {
    // Enable message ordering for this publisher
    messageOrdering: true,
  });

  const publisher = topic.publisher();

  for (const message of messages) {
    const dataBuffer = Buffer.from(message);
    try {
      const messageId = await publisher.publish(dataBuffer, {orderingKey});
      console.log(`Message ${messageId} published.`);
    } catch (error) {
      console.error(`Received error while publishing: ${error.message}`);
      process.exit(1); // Exit in case of error
    }
  }
}

// Define the messages you want to send
const messages = [
  'First message',
  'Second message',
  'Third message'
];

publishOrderedMessages(topicName, orderingKey, messages).catch(console.error);
