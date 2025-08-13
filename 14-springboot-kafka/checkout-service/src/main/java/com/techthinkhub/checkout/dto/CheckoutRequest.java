package com.techthinkhub.checkout.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;

@Data
public class CheckoutRequest {
  @NotNull private String userId;
  @Positive private long amount;
  @NotNull private String paymentMethod; // VA/QRIS/CARD
}
