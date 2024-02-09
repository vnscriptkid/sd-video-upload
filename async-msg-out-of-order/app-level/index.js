const messageBuffer = [];
const currentSequenceNumber = 0;
let expectedSequenceNumber = 1; // The next expected sequence number

function receiveMessage(message) {
    // Add the message to the buffer if it's not in order
    if (message.sequenceNumber !== expectedSequenceNumber) {
      messageBuffer.push(message);
      messageBuffer.sort((a, b) => a.sequenceNumber - b.sequenceNumber); // Keep buffer sorted
      return;
    }
  
    // Process the message
    console.log(`Processed: `, message);
    expectedSequenceNumber++;
  
    // Check buffer for the next message in sequence
    while (messageBuffer.length > 0 && messageBuffer[0].sequenceNumber === expectedSequenceNumber) {
      const nextMessage = messageBuffer.shift();
      console.log(`Processed from buffer: `, nextMessage);
      expectedSequenceNumber++;
    }
  }
  
  // Simulated message receiving (out of order)
  receiveMessage({ content: 'Message 3', sequenceNumber: 3 });
  receiveMessage({ content: 'Message 1', sequenceNumber: 1 }); // This will trigger processing of message 1
  receiveMessage({ content: 'Message 2', sequenceNumber: 2 }); // This will get processed immediately after message 1