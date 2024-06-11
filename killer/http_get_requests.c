#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <time.h>

#define BUFFER_SIZE 1024

int create_tcp_socket();
char *get_ip(const char *host);
char *build_get_query(const char *host, const char *page);
void send_requests(const char *url, int req_per_sec);

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <URL> <Requests per second>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *url = argv[1];
    int req_per_sec = atoi(argv[2]);

    send_requests(url, req_per_sec);

    return 0;
}

void send_requests(const char *url, int req_per_sec)
{
    char *get_request = build_get_query(url, "/");
    int sockfd = create_tcp_socket();
    const char *ip = get_ip(url);

    struct sockaddr_in dest_addr;
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(80);
    inet_pton(AF_INET, ip, &(dest_addr.sin_addr));

    while (1)
    {
        clock_t start_time = clock();
        int requests_sent = 0;

        while ((double)(clock() - start_time) / CLOCKS_PER_SEC < 1)
        {
            if (connect(sockfd, (struct sockaddr *)&dest_addr, sizeof(struct sockaddr)) == -1)
            {
                perror("Connect");
                exit(EXIT_FAILURE);
            }

            if (send(sockfd, get_request, strlen(get_request), 0) == -1)
            {
                perror("Send");
                exit(EXIT_FAILURE);
            }

            requests_sent++;
        }

        printf("Requests sent in 1 second: %d\n", requests_sent);
        int sleep_time_micro = (1000000 / req_per_sec) - (int)((double)(clock() - start_time) / CLOCKS_PER_SEC * 1000000);
        if (sleep_time_micro > 0)
        {
            usleep(sleep_time_micro);
        }
    }

    free(get_request);
    close(sockfd);
}

int create_tcp_socket()
{
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1)
    {
        perror("Socket");
        exit(EXIT_FAILURE);
    }
    return sockfd;
}

char *get_ip(const char *host)
{
    struct hostent *hent;
    hent = gethostbyname(host);
    if (hent == NULL)
    {
        herror("Can't get IP");
        exit(EXIT_FAILURE);
    }
    return inet_ntoa(*(struct in_addr *)hent->h_addr);
}

char *build_get_query(const char *host, const char *page)
{
    const char *template = "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n";
    int size = strlen(template) + strlen(page) + strlen(host) - 4;
    char *query = (char *)malloc(size);
    sprintf(query, template, page, host);
    return query;
}
