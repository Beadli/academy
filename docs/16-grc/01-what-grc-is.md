---
title: "16.1 What GRC is, and why your lab is a system"
sidebar_position: 1
---

# 16.1 What GRC is, and why your lab is a system

Three words that get said together and mean quite different things.

**Governance** is who decides. Who sets the rules, who can approve an
exception, who is accountable when it goes wrong. Most compliance failures
that look technical are governance failures underneath: nobody owned the
decision, so nobody made it.

**Risk** is what could go wrong and how much you care. Not a list of threats,
but a set of decisions about which ones you are going to spend money on and
which you will accept. You did this already in lesson 13.8 when you wrote a
risk acceptance.

**Compliance** is proving it, to somebody outside your own head. An auditor,
a regulator, a customer's security questionnaire, or a court.

**The order matters.** Governance decides, risk work informs the decisions,
compliance demonstrates them. Organisations that start at compliance produce
documents describing a system nobody governs, which is where the paperwork
reputation comes from.

## The only question an assessor is asking

Strip away the vocabulary and every framework asks the same three-part
question about every control:

1. **What are you supposed to be doing?** The policy or requirement.
2. **What are you actually doing?** The implementation.
3. **How do I know?** The evidence.

If that shape looks familiar, it should. It is the same shape as the three
questions this course has asked in every lesson since Module 0: what are we
doing, why, and how do we know it worked.

**That is not a coincidence.** An assessable system and a well-taught
procedure have the same requirement: a claim, and something that
substantiates it. You have been producing audit evidence for fifteen modules
without calling it that.

## Why "implemented" is the word that carries the weight

Lesson 4.6 made this point when you tested segmentation:

> Notice what made it assessable: not the fact that a firewall exists, but
> that you can state the policy, show the rules that implement it, and
> produce evidence you tested both directions. That's the difference between
> a control that's implemented and one that's merely installed.

Four states a control can be in, and confusing them is the most common
failure in self-assessment:

| State | What it means |
|---|---|
| **Not implemented** | You are not doing it. Honest, and it goes in the POA&M |
| **Installed** | The technology exists. Nobody configured it, nobody checks it |
| **Implemented** | It is configured, working, and doing the job |
| **Implemented and evidenced** | All of the above, and you can prove it to somebody else |

**Only the last one passes an assessment.** A firewall with default rules is
installed. A firewall with a written policy, rules that implement it, and a
test result showing traffic blocked in one direction and allowed in the other
is implemented and evidenced. You produced exactly that in lesson 4.6.

## Your lab is a system, and here is why that matters

A **system**, for assessment purposes, is a set of resources that are managed
together and share a boundary. Your lab qualifies: DC01, DC02, UBNT01, FW01,
SUBCA01, ROOTCA01, KALI01, one network, one administrator.

Give it a name. Throughout this module it is **GSS-1**.

Naming it sounds like ceremony and it does real work: **it forces you to say
what is in it and what is not**, which is the next lesson's job and the
single most consequential decision in any assessment.

## Define the boundary

The **authorisation boundary** is what you are assessing and taking
responsibility for. Everything inside it is yours to secure. Everything
outside it is somebody else's, and how you connect to it becomes an interface
you have to describe.

**Boundary decisions are where assessments are won and lost**, because a
boundary drawn too wide makes the work impossible and one drawn too narrow
hides the risk. Real organisations argue about this for weeks.

Write yours. Create `Projects/gss1-boundary.md` in your vault:

```markdown
# GSS-1: system boundary

## Inside the boundary
| Component | Address | Role | Module built |
|---|---|---|---|
| FW01 | 10.10.10.254 | Perimeter firewall, DHCP, DNS forwarding | 4 |
| DC01 | 10.10.10.10 | Domain controller, DNS, PKI-integrated | 5 |
| DC02 | 10.10.10.11 | Second domain controller | 5 |
| UBNT01 | 10.10.10.20 | Docker host: Gitea, monitoring, scanning | 6 |
| SUBCA01 | 10.10.10.30 | Issuing certificate authority | 7 |
| ROOTCA01 | offline | Offline root CA, powered off | 7 |
| KALI01 | 10.10.10.50 | Authorised testing host (Tier 1 address; Tier 2, use your outer-segment one) | 4 |

## The network
10.10.10.0/24, a single segment behind FW01.

## Outside the boundary, and how we connect to it
| External thing | Interface | Who owns the risk |
|---|---|---|
| The internet | Outbound only via FW01 NAT. No inbound ports | ISP and me at the boundary |
| Entra ID tenant | Entra Connect sync, outbound HTTPS from DC01 | Microsoft, jointly |
| GitHub | Outbound HTTPS, journal backup | GitHub |
| Container registries | Outbound HTTPS, image pulls | Registry operators |
| Tailscale overlay | Optional; disabled during testing | Tailscale |
| The host laptop / hypervisor | Hosts every VM | Me, but NOT assessed here |

## Explicitly excluded, and why
- **The host laptop and hypervisor.** Every VM depends on it, so this
  is a real dependency and a real limitation of this assessment. It is
  excluded because it is a personal general-purpose machine, not
  managed as part of GSS-1. Recorded as a risk rather than ignored.
- **My home network.** Separate, not managed as part of this system.
```

**That last section is the important one**, and it is what separates an
honest boundary from a convenient one. Excluding something is legitimate.
**Excluding it silently is not.** The hypervisor genuinely underpins
everything in GSS-1, so naming it as an excluded dependency and carrying it
as a risk is the professional move; quietly leaving it off the diagram is
how real assessments end up describing a system that does not exist.

## What the deliverables are called

Three documents come out of this module, and knowing the names is worth
actual money in an interview:

- **SSP, System Security Plan.** What the system is, and how each control is
  implemented. The main document. Lesson 16.8.
- **POA&M, Plan of Action and Milestones.** The gaps, with owners and dates.
  Pronounced "po-am". Lesson 16.7.
- **Authorisation memo.** A named person accepting the residual risk and
  permitting the system to operate. Lesson 16.8.

**The POA&M is the one that surprises people.** A system with a POA&M full of
honestly recorded gaps and realistic dates is in far better shape than one
claiming everything is perfect, and assessors read it that way. An empty
POA&M is a red flag, not a gold star.

## What you take from this

Three words with distinct meanings, the four states a control can be in, and
a written boundary for GSS-1 that says what you are excluding and why.

Next lesson decides how much any of it matters.
