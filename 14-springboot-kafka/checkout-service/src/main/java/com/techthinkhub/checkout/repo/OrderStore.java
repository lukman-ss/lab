package com.techthinkhub.checkout.repo;

import com.techthinkhub.checkout.domain.OrderStatus;
import org.springframework.stereotype.Repository;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

@Repository
public class OrderStore {
  private final Map<String, OrderStatus> store = new ConcurrentHashMap<>();
  public void put(String orderId, OrderStatus status) { store.put(orderId, status); }
  public OrderStatus get(String orderId) { return store.get(orderId); }
}
