/**
 * Exemplo de automação Tinder em Java/Spring Boot
 * Padrão encontrado em repositórios como jayram0402/Tinder-Automation
 *
 * Frameworks: Spring Boot, Spring WebClient
 * Padrão: REST API + background jobs
 */

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import java.util.*;
import java.time.Instant;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Repository;
import org.springframework.data.repository.CrudRepository;
import jakarta.persistence.*;

// ======================== MODELOS ========================

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "profiles")
class TinderProfile {
  @Id
  private String userId;
  private String name;
  private Integer age;
  private String bio;
  private String location;
  private Double latitude;
  private Double longitude;
  @JsonProperty("photo_urls")
  private List<String> photoUrls;
  private Long createdAt;
  private Long updatedAt;
}

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "matches")
class TinderMatch {
  @Id
  @GeneratedValue(strategy = GenerationType.UUID)
  private String id;
  private String matchId;
  private String matchName;
  private Long matchedAt;
  private Boolean messaged = false;
  private String lastMessage;
}

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "automation_logs")
class AutomationLog {
  @Id
  @GeneratedValue(strategy = GenerationType.UUID)
  private String id;
  private Integer likesCount = 0;
  private Integer passCount = 0;
  private Integer matchesCount = 0;
  private Long startTime;
  private Long endTime;
  private String status; // RUNNING, COMPLETED, ERROR
  private String errorMessage;
}

// ======================== REPOSITORIES ========================

interface ProfileRepository extends CrudRepository<TinderProfile, String> {
}

interface MatchRepository extends CrudRepository<TinderMatch, String> {
  List<TinderMatch> findByMessaged(Boolean messaged);
}

interface AutomationLogRepository extends CrudRepository<AutomationLog, String> {
}

// ======================== DTOs ========================

@Data
@NoArgsConstructor
@AllArgsConstructor
class RecommendationResponse {
  private List<TinderProfile> results;
  private String nextBatchId;
}

@Data
@NoArgsConstructor
@AllArgsConstructor
class LikeResponse {
  private Boolean liked;
  private Boolean matched;
  private String matchId;
}

@Data
@NoArgsConstructor
@AllArgsConstructor
class MessageRequest {
  private String matchId;
  private String message;
}

// ======================== SERVIÇOS ========================

@Service
class TinderAPIService {
  private final WebClient webClient;
  private final String authToken;
  private static final String BASE_URL = "https://api.gotinder.com";

  @Autowired
  public TinderAPIService(String authToken) {
    this.authToken = authToken;
    this.webClient = WebClient.builder()
        .baseUrl(BASE_URL)
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .defaultHeader("X-Auth-Token", authToken)
        .build();
  }

  public RecommendationResponse getRecommendations() {
    return webClient.get()
        .uri("/recs")
        .retrieve()
        .bodyToMono(RecommendationResponse.class)
        .block();
  }

  public LikeResponse likeProfile(String userId) {
    return webClient.post()
        .uri("/like/{userId}", userId)
        .retrieve()
        .bodyToMono(LikeResponse.class)
        .block();
  }

  public void passProfile(String userId) {
    webClient.post()
        .uri("/pass/{userId}", userId)
        .retrieve()
        .bodyToMono(Void.class)
        .block();
  }

  public void sendMessage(String matchId, String message) {
    webClient.post()
        .uri("/user/matches/{matchId}", matchId)
        .bodyValue(new MessageRequest(matchId, message))
        .retrieve()
        .bodyToMono(Void.class)
        .block();
  }
}

@Service
@EnableScheduling
class TinderAutomationService {

  @Autowired private TinderAPIService apiService;
  @Autowired private ProfileRepository profileRepository;
  @Autowired private MatchRepository matchRepository;
  @Autowired private AutomationLogRepository logRepository;

  private AutomationLog currentLog;

  @Scheduled(cron = "0 0 */6 * * *") // A cada 6 horas
  public void runAutoSwiping() {
    currentLog = new AutomationLog();
    currentLog.setStartTime(System.currentTimeMillis());
    currentLog.setStatus("RUNNING");
    logRepository.save(currentLog);

    try {
      executeAutoSwipe();
      currentLog.setStatus("COMPLETED");
    } catch (Exception e) {
      currentLog.setStatus("ERROR");
      currentLog.setErrorMessage(e.getMessage());
    }

    currentLog.setEndTime(System.currentTimeMillis());
    logRepository.save(currentLog);
  }

  private void executeAutoSwipe() {
    int likeCount = 0;
    int passCount = 0;

    RecommendationResponse recs = apiService.getRecommendations();

    if (recs == null || recs.getResults() == null) {
      return;
    }

    for (TinderProfile profile : recs.getResults()) {
      // Salva perfil
      profileRepository.save(profile);

      // Avalia se faz swipe right
      if (shouldLike(profile)) {
        try {
          LikeResponse response = apiService.likeProfile(profile.getUserId());
          likeCount++;

          if (response.getMatched()) {
            TinderMatch match = new TinderMatch(
                null,
                response.getMatchId(),
                profile.getName(),
                System.currentTimeMillis(),
                false,
                null
            );
            matchRepository.save(match);

            // Envia mensagem automática
            if (shouldAutoMessage()) {
              String message = generateOpener(profile);
              apiService.sendMessage(response.getMatchId(), message);
              match.setMessaged(true);
              match.setLastMessage(message);
              matchRepository.save(match);
            }
          }
        } catch (Exception e) {
          System.err.println("Erro ao fazer like: " + e.getMessage());
        }
      } else {
        try {
          apiService.passProfile(profile.getUserId());
          passCount++;
        } catch (Exception e) {
          System.err.println("Erro ao fazer pass: " + e.getMessage());
        }
      }

      // Delay para não parecer bot (2-5 segundos)
      try {
        Thread.sleep(2000 + (long)(Math.random() * 3000));
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
      }
    }

    currentLog.setLikesCount(likeCount);
    currentLog.setPassCount(passCount);
  }

  private boolean shouldLike(TinderProfile profile) {
    // Lógica de avaliação
    // Em produção: usar modelo IA
    if (profile.getAge() == null) return false;
    return profile.getAge() >= 20 && profile.getAge() <= 35;
  }

  private boolean shouldAutoMessage() {
    return true; // Configurável
  }

  private String generateOpener(TinderProfile profile) {
    // Em produção: integrar com ChatGPT
    List<String> openers = Arrays.asList(
        "Oi " + profile.getName() + "! 👋",
        "Sua foto de perfil é incrível! 😄",
        "Que interessante sua bio! Conte mais sobre você 😊"
    );
    return openers.get((int)(Math.random() * openers.size()));
  }
}

// ======================== CONTROLLERS ========================

@org.springframework.web.bind.annotation.RestController
@org.springframework.web.bind.annotation.RequestMapping("/api")
class AutomationController {

  @Autowired private AutomationLogRepository logRepository;
  @Autowired private MatchRepository matchRepository;

  @org.springframework.web.bind.annotation.GetMapping("/stats")
  public Map<String, Object> getStats() {
    List<AutomationLog> logs = (List<AutomationLog>) logRepository.findAll();

    if (logs.isEmpty()) {
      return Map.of("message", "Nenhuma automação iniciada");
    }

    AutomationLog lastRun = logs.get(logs.size() - 1);
    long duration = lastRun.getEndTime() - lastRun.getStartTime();

    return Map.of(
        "totalLikes", lastRun.getLikesCount(),
        "totalPass", lastRun.getPassCount(),
        "totalMatches", lastRun.getMatchesCount(),
        "duration", duration / 1000 + "s",
        "status", lastRun.getStatus()
    );
  }

  @org.springframework.web.bind.annotation.GetMapping("/matches")
  public List<TinderMatch> getMatches() {
    return matchRepository.findByMessaged(false);
  }
}

// ======================== APLICAÇÃO ========================

@SpringBootApplication
public class TinderAutomationApp {
  public static void main(String[] args) {
    SpringApplication.run(TinderAutomationApp.class, args);
    System.out.println("✅ Tinder Automation API rodando!");
    System.out.println("📊 Padrões Java encontrados:");
    System.out.println("1. Spring Boot REST API");
    System.out.println("2. WebClient para API calls");
    System.out.println("3. JPA/Hibernate para persistência");
    System.out.println("4. @Scheduled para jobs automáticos");
    System.out.println("5. Service + Repository pattern");
  }
}

/*
 * Configuração necessária (application.yml):
 *
 * spring:
 *   datasource:
 *     url: jdbc:mysql://localhost:3306/tinder_automation
 *     username: root
 *     password: senha
 *   jpa:
 *     hibernate:
 *       ddl-auto: update
 *
 * tinder:
 *   auth-token: seu_token_aqui
 */
