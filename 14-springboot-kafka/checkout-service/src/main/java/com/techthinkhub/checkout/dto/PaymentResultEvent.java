package com.techthinkhub.checkout.dto;

import lombok.*;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class PaymentResultEvent {
  public enum Status { SUCCESS, FAILED }
  private String orderId;
  private Status status;
  private String txId;
  private String reason;
  private long timestamp;
}
