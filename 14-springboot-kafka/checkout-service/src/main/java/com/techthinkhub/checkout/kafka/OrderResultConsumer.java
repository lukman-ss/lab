package com.techthinkhub.checkout.kafka;

import com.techthinkhub.checkout.domain.OrderStatus;
import com.techthinkhub.checkout.dto.PaymentResultEvent;
import com.techthinkhub.checkout.repo.OrderStore;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class OrderResultConsumer {
  private final OrderStore store;

  @KafkaListener(topics = "${app.topics.paymentCompleted}", groupId = "order-updater")
  public void onCompleted(PaymentResultEvent evt) {
    var st = evt.getStatus() == PaymentResultEvent.Status.SUCCESS ? OrderStatus.PAID : OrderStatus.FAILED;
    store.put(evt.getOrderId(), st);
    log.info("Order {} -> {}", evt.getOrderId(), st);
  }
}
