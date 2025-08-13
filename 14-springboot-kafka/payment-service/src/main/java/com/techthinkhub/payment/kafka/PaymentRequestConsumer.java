package com.techthinkhub.payment.kafka;

import com.techthinkhub.payment.dto.PaymentRequestedEvent;
import com.techthinkhub.payment.dto.PaymentResultEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.Random;

@Slf4j
@Component
@RequiredArgsConstructor
public class PaymentRequestConsumer {
  private final PaymentResultProducer producer;
  private final Random rnd = new Random();

  @KafkaListener(topics = "${app.topics.paymentRequested}", groupId = "payment-service")
  public void onRequested(PaymentRequestedEvent evt) {
    log.info("Processing payment: order={} amount={} method={}",
        evt.getOrderId(), evt.getAmount(), evt.getMethod());

    try { Thread.sleep(200 + rnd.nextInt(1000)); } catch (InterruptedException ignored) {}

    boolean ok = rnd.nextDouble() > 0.2; // 80% sukses
    PaymentResultEvent result = ok
      ? PaymentResultEvent.builder()
          .orderId(evt.getOrderId())
          .status(PaymentResultEvent.Status.SUCCESS)
          .txId("TX-" + Math.abs(rnd.nextLong()))
          .timestamp(System.currentTimeMillis())
          .build()
      : PaymentResultEvent.builder()
          .orderId(evt.getOrderId())
          .status(PaymentResultEvent.Status.FAILED)
          .txId("TX-" + Math.abs(rnd.nextLong()))
          .reason("Insufficient funds (simulated)")
          .timestamp(System.currentTimeMillis())
          .build();

    producer.publish(result);
  }
}
