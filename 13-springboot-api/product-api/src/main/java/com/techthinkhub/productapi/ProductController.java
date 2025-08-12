package com.techthinkhub.productapi;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@RestController
@RequestMapping("/api/products")
public class ProductController {

  private final Map<Long, Product> db = new ConcurrentHashMap<>();
  private final AtomicLong seq = new AtomicLong(0);

  @GetMapping
  public List<Product> all() {
    return db.values().stream()
        .sorted(Comparator.comparing(Product::id))
        .toList();
  }

  @GetMapping("/{id}")
  public ResponseEntity<Product> one(@PathVariable Long id) {
    Product p = db.get(id);
    return p != null ? ResponseEntity.ok(p) : ResponseEntity.notFound().build();
  }

  @PostMapping
  public ResponseEntity<Product> create(@RequestBody Product payload) {
    if (payload == null || payload.name() == null || payload.name().isBlank()) {
      return ResponseEntity.badRequest().build();
    }
    long id = seq.incrementAndGet();
    Product p = new Product(id, payload.name(), payload.price(), payload.stock());
    db.put(id, p);
    return ResponseEntity.status(HttpStatus.CREATED).body(p);
  }

  @PutMapping("/{id}")
  public ResponseEntity<Product> update(@PathVariable Long id, @RequestBody Product payload) {
    if (!db.containsKey(id)) return ResponseEntity.notFound().build();
    if (payload == null || payload.name() == null || payload.name().isBlank()) {
      return ResponseEntity.badRequest().build();
    }
    Product p = new Product(id, payload.name(), payload.price(), payload.stock());
    db.put(id, p);
    return ResponseEntity.ok(p);
  }

  @DeleteMapping("/{id}")
  public ResponseEntity<Void> delete(@PathVariable Long id) {
    return db.remove(id) != null ? ResponseEntity.noContent().build()
                                 : ResponseEntity.notFound().build();
  }
}
