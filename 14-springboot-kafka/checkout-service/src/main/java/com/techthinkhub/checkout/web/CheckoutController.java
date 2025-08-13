package com.techthinkhub.checkout.web;

import com.techthinkhub.checkout.domain.OrderStatus;
import com.techthinkhub.checkout.dto.CheckoutRequest;
import com.techthinkhub.checkout.dto.PaymentRequestedEvent;
import com.techthinkhub.checkout.repo.OrderStore;
import com.techthinkhub.checkout.kafka.PaymentProducer;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class CheckoutController {
  private final PaymentProducer producer;
  private final OrderStore store;

  @PostMapping("/checkout")
  public Map<String, Object> checkout(@Valid @RequestBody CheckoutRequest body) {
    String orderId = UUID.randomUUID().toString();
    store.put(orderId, OrderStatus.PENDING_PAYMENT);

    producer.publishRequested(PaymentRequestedEvent.builder()
      .orderId(orderId)
      .userId(body.getUserId())
      .amount(body.getAmount())
      .method(body.getPaymentMethod())
      .timestamp(System.currentTimeMillis())
      .build());

    return Map.of("orderId", orderId, "status", "PENDING_PAYMENT");
  }

  @GetMapping("/orders/{orderId}")
  public Map<String, Object> get(@PathVariable String orderId) {
    var st = store.get(orderId);
    return Map.of("orderId", orderId, "status", st == null ? "NOT_FOUND" : st.name());
  }
}
