package com.techthinkhub.checkout.kafka;

import com.techthinkhub.checkout.dto.PaymentRequestedEvent;
import com.techthinkhub.checkout.dto.PaymentResultEvent;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class PaymentProducer {
  private final KafkaTemplate<String, Object> kafka;
  @Value("${app.topics.paymentRequested}") private String topicRequested;
  @Value("${app.topics.paymentCompleted}") private String topicCompleted;

  public void publishRequested(PaymentRequestedEvent evt) {
    kafka.send(topicRequested, evt.getOrderId(), evt);
  }
  public void publishCompleted(PaymentResultEvent evt) {
    kafka.send(topicCompleted, evt.getOrderId(), evt);
  }
}
