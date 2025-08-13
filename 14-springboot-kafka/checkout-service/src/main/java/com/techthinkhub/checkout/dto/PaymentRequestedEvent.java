package com.techthinkhub.checkout.dto;

import lombok.*;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class PaymentRequestedEvent {
  private String orderId;
  private String userId;
  private long amount;
  private String method;
  private long timestamp;
}
