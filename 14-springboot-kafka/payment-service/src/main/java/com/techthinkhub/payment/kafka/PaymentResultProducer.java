package com.techthinkhub.payment.kafka;

import com.techthinkhub.payment.dto.PaymentResultEvent;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class PaymentResultProducer {
  private final KafkaTemplate<String, Object> kafka;
  @Value("${app.topics.paymentCompleted}") private String topicCompleted;

  public void publish(PaymentResultEvent evt) {
    kafka.send(topicCompleted, evt.getOrderId(), evt);
  }
}
