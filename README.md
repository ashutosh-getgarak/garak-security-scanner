# Garak Security Scanner

![GitHub release](https://img.shields.io/github/v/release/ashutosh-getgarak/garak-security-scanner)
[![CI](https://github.com/ashutosh-getgarak/garak-security-scanner/workflows/CI/badge.svg)](https://github.com/ashutosh-getgarak/garak-security-scanner/actions)

A GitHub Action that runs comprehensive AI security scans in your CI/CD pipeline using [Garak](https://www.getgarak.com/) - the leading LLM vulnerability scanner.

Automatically detect:
- 🛡️ Prompt injection attacks
- 🔒 Security vulnerabilities
- 🔐 Privacy leaks
- ☠️ Toxicity and harmful content
- 🎭 DAN (Do Anything Now) jailbreaks
- 🧠 Hallucination risks
- ⚡ Performance issues
- 🎯 Robustness weaknesses
- ⚖️ Ethical concerns
- 🏷️ Stereotype biases

## Quick Start

### 1. Set up secrets

Add these secrets to your GitHub repository:
- Go to **Settings → Secrets and variables → Actions → New repository secret**
- Add `GARAK_API_KEY` - Your Garak API key ([sign up at getgarak.com](https://www.getgarak.com/))
- Add `X_API_KEY` - API key for the endpoint you're testing (e.g., Anthropic, OpenAI)

### 2. Create workflow file

Create `.github/workflows/garak-security-scan.yml`:

```yaml
name: AI Security Scan

on:
  push:
    branches: [main, master, develop]
  pull_request:
    branches: [main, master, develop]
  workflow_dispatch:

jobs:
  garak-scan:
    runs-on: ubuntu-latest
    name: Garak Security Analysis

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Garak Security Scan
        uses: ashutosh-getgarak/garak-security-scanner@v1
        with:
          api_key: ${{ secrets.GARAK_API_KEY }}
          endpoint: https://api.anthropic.com/v1/messages
          target_api_key: ${{ secrets.TARGET_API_KEY }}
          probes: dan,security,privacy,toxicity,hallucination,performance,robustness,ethics,stereotypes
          score_threshold: 80

      - name: Upload scan results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: garak-security-report
          path: garak-report-*.json
          retention-days: 30
```

### 3. Run and monitor

The action will automatically:
1. ✅ Execute comprehensive security scans on every push/PR
2. 📊 Generate detailed vulnerability reports
3. ⚡ Fail the build if security score < threshold
4. 📦 Upload results as artifacts
5. 💬 Comment on PRs with scan results


## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `api_key` | Garak API key | Yes | - |
| `endpoint` | Target API endpoint to scan | Yes | - |
| `model_id` | Model identifier (if applicable) | No | `''` |
| `probes` | Comma-separated probe categories | No | `dan,security,privacy,toxicity` |
| `generator_mode` | Generator mode (e.g., rest) | No | `rest` |
| `parallel_attempts` | Number of parallel scan attempts | No | `4` |
| `response_json_path` | JSON path for response extraction | No | `$.content[0].text` |
| `target_api_key` | API key for target endpoint | No | `''` |
| `timeout_minutes` | Max scan timeout in minutes | No | `60` |
| `score_threshold` | Minimum passing score (0-100) | No | `80` |
| `poll_interval` | Seconds between status checks | No | `10` |

## Outputs

| Output | Description |
|--------|-------------|
| `scan_id` | Unique scan identifier |
| `security_score` | Overall security score (0-100) |
| `vulnerabilities_found` | Number of vulnerabilities detected |
| `report_url` | URL to detailed scan report |
| `status` | Final status (passed/failed) |

## Probe Categories

- **dan** - Do Anything Now jailbreak attempts
- **security** - Security vulnerability testing
- **privacy** - Privacy leak detection
- **toxicity** - Harmful and toxic content
- **hallucination** - Factual accuracy and hallucination risks
- **performance** - Performance and reliability issues
- **robustness** - Model robustness under adversarial conditions
- **ethics** - Ethical alignment testing
- **stereotypes** - Bias and stereotype detection

## Advanced Examples

### Custom probe selection

```yaml
- uses: ashutosh-getgarak/garak-security-scanner@v1
  with:
    api_key: ${{ secrets.GARAK_API_KEY }}
    endpoint: https://api.openai.com/v1/chat/completions
    target_api_key: ${{ secrets.OPENAI_API_KEY }}
    probes: security,privacy,ethics
    score_threshold: 90
```

### Multiple endpoint testing

```yaml
jobs:
  scan-anthropic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ashutosh-getgarak/garak-security-scanner@v1
        with:
          api_key: ${{ secrets.GARAK_API_KEY }}
          endpoint: https://api.anthropic.com/v1/messages
          target_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

  scan-openai:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ashutosh-getgarak/garak-security-scanner@v1
        with:
          api_key: ${{ secrets.GARAK_API_KEY }}
          endpoint: https://api.openai.com/v1/chat/completions
          target_api_key: ${{ secrets.OPENAI_API_KEY }}
```

### PR comment integration

```yaml
- name: Run Garak Security Scan
  id: garak
  uses: garaksecurity/garak-security-scanner@v1
  with:
    api_key: ${{ secrets.GARAK_API_KEY }}
    endpoint: ${{ secrets.API_ENDPOINT }}
    target_api_key: ${{ secrets.TARGET_API_KEY }}

- name: Comment PR
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## 🛡️ Garak Security Scan Results\n\n` +
              `**Score:** ${{ steps.garak.outputs.security_score }}/100\n` +
              `**Vulnerabilities:** ${{ steps.garak.outputs.vulnerabilities_found }}\n` +
              `**Status:** ${{ steps.garak.outputs.status }}\n\n` +
              `[View Full Report](${{ steps.garak.outputs.report_url }})`
      })
```

## Supported Endpoints

Garak supports security scanning for all major LLM providers:

- **OpenAI** - GPT-4, GPT-3.5, and all OpenAI models
- **Anthropic Claude** - Claude 3.5 Sonnet, Claude 3 Opus, and all Claude models
- **AWS Bedrock** - Amazon's managed AI service with multiple model providers
- **Cohere** - Command, Generate, and Embed models
- **Google Gemini** - Gemini Pro, Gemini Ultra, and PaLM models
- **Hugging Face** - Models hosted on Hugging Face Hub
- **LiteLLM** - Universal LLM gateway supporting 100+ providers
- **Llama.cpp** - Local LLaMA model deployments
- **Mistral AI** - Mistral 7B, Mixtral, and all Mistral models
- **Ollama** - Local model runtime and management
- **Replicate** - Cloud-hosted model API
- **Custom REST APIs** - Any LLM endpoint with standard request/response formats

## Troubleshooting

### Scan timeouts

Increase the timeout for longer scans:
```yaml
timeout_minutes: 120
```

### Authentication errors

Verify your secrets are correctly set:
```bash
echo ${{ secrets.GARAK_API_KEY }} | wc -c  # Should be > 10
```

### Custom response parsing

For non-standard API responses, adjust the JSON path:
```yaml
response_json_path: $.choices[0].message.content
```

## Security Best Practices

- ✅ Store API keys in GitHub Secrets, never in code
- ✅ Use repository secrets for private repos
- ✅ Use environment secrets for organization-wide keys
- ✅ Rotate API keys regularly
- ✅ Review scan reports for all vulnerabilities
- ✅ Set appropriate score thresholds for your use case

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For support, visit [www.getgarak.com](https://www.getgarak.com/) or open an issue in this repository.

## License

Proprietary - © Garak Inc. All rights reserved.

## Future Enhancements

- [ ] Scheduled background scans with cron triggers
- [ ] Slack/Teams notification integrations
- [ ] Custom report formatting and branding
- [ ] Baseline comparison and regression detection
- [ ] Multi-model comparative analysis
- [ ] SARIF format output for GitHub Code Scanning
- [ ] Automatic issue creation for critical vulnerabilities
- [ ] Integration with GitHub Security tab
- [ ] Support for custom probe development
- [ ] Historical trend analysis and dashboards

---

**Protect your AI applications from security threats. Start scanning today!** 🚀
