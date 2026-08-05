# Technical Test, Backend Python / Django Developer (apprenticeship)

Welcome, and thank you for your interest in joining Codoc.

The purpose of this test is to give us a sense of how you work on a Django / Django REST
Framework project. **We do not expect it to be perfect, or even finished.** What we care
about is:

- your ability to find your way around the official documentation on your own;
- how you reason and prioritise when time is short;
- your ability to explain what you did and why.

**Suggested duration: 1 to 2 hours.** Please do not spend more than 2 hours of actual
work on it. If you do not finish, that is fine, just tell us so in your submission (see
the [Deliverable](#6-deliverable) section).

---

## 1. Getting started

The project skeleton is provided in this archive. It contains a Django project already
configured with Django REST Framework and a SQLite database.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Generate the initial migration, then create the database
python manage.py makemigrations
python manage.py migrate

# Load a starter dataset (10 books and a few loans)
python manage.py loaddata initial

# Run the server
python manage.py runserver
```

The `library/migrations/` directory is intentionally empty. Generating the initial
migration from the provided models is up to you, as is generating the following ones if
you change those models.

The API will be served under the `http://127.0.0.1:8000/api/` prefix. No route is declared
there yet, so a 404 at that address is the expected behaviour on a fresh start.

If a setup problem blocks you for more than 15 minutes, get in touch. That is not what we
are trying to assess.

---

## 2. What you are allowed to use

**Anything.** This is not a memory exercise. Nobody on the team writes code
without a documentation tab open next to them.

So feel free to use:

- the official [Django](https://docs.djangoproject.com/en/stable/) and
  [Django REST Framework](https://www.django-rest-framework.org/) documentation. These are
  our daily tools, and knowing how to navigate them is exactly one of the skills we are
  looking for;
- help sites (Stack Overflow, blogs, tutorials, forums, and so on);
- generative AI assistants (Claude, ChatGPT, Copilot, and so on);
- any third-party package you like (`django-filter`, `drf-spectacular`, etc.), as long as
  you add it to `requirements.txt`.

There is one condition, and it is a firm one: **you must understand and be able to justify
every line you submit.** We will go through it with you during the debrief interview. Code
you cannot explain will be treated as not submitted.

We also ask that you mention in your `description.md` which tools actually helped you, and
what you delegated to them. This is information, not a penalty. We are looking for someone
who knows how to use their tools, not someone who hides them.

---

## 3. The subject

We want to expose a small REST API to manage **a library and the loans of its books**.

The skeleton contains a `library` application in which **the models are already written**.
Take the time to read `library/models.py` before you start. Everything else (serializers,
views, routes) is up to you.

Two things worth knowing as you read the models:

- A loan is **ongoing** as long as its return date has not been set.
- There is deliberately **no `available` field on `Book`**. Availability is derived from
  the ongoing loans. How to expose it in the API is up to you.

You may change these models if you feel the need (adding an index, a constraint, a method,
and so on), as long as you generate the matching migration and explain why in your
submission.

### The business rule

> A book that is already on loan and has not been returned yet cannot be borrowed a second
> time.

This is the heart of the exercise. How you implement this rule, and where you put it, is
of particular interest to us.

---

## 4. What we ask of you

| # | Method and URL | Expected |
|---|---|---|
| 1 | `GET /api/books/` | List of books, **paginated**. Must allow **filtering on currently available books** and **searching by title or author**. |
| 2 | `POST /api/books/` | Creates a book, with **validation** of the submitted data (at a minimum: unique ISBN, sensible publication year). Errors must produce an explicit response. |
| 3 | `GET /api/books/{id}/` | Details of a book, including its availability. |
| 4 | `DELETE /api/books/{id}/` | Deletes a book. **What should happen if the book is currently on loan?** That is yours to decide and to justify. |
| 5 | `POST /api/books/{id}/borrow/` | Creates a loan for this book. Must cleanly refuse if the book is already on loan. |
| 6 | `POST /api/loans/{id}/return/` | Records the return of a book. Must refuse if the loan is already closed. |

The URLs are indicative. You may adapt them if you justify your choice.

You are free to pick the implementation style: `APIView`, `ViewSet`, generic views, the
choice is yours, as long as you can explain it.

### Example requests and responses

The examples below describe the expected behaviour. **The exact shape of the response
bodies is indicative**, we will not compare keys one by one. The HTTP status codes, on the
other hand, must be consistent and you must be able to justify them.

#### Retrieve a book, `GET /api/books/3/`

```http
HTTP/1.1 200 OK
```
```json
{
  "id": 3,
  "title": "Brave New World",
  "author": "Aldous Huxley",
  "isbn": "9782266283038",
  "publication_year": 1932,
  "available": true
}
```

#### Borrow a book, `POST /api/books/3/borrow/`

```json
{
  "borrower": "camille.martin@example.com",
  "due_date": "2026-08-17"
}
```

The book is available, the loan is created:

```http
HTTP/1.1 201 Created
```
```json
{
  "id": 12,
  "book": 3,
  "borrower": "camille.martin@example.com",
  "loan_date": "2026-08-03",
  "due_date": "2026-08-17",
  "return_date": null
}
```

The book is already on loan:

```http
HTTP/1.1 409 Conflict
```
```json
{
  "detail": "This book is already on loan and has not been returned yet."
}
```

> `409` is not the only defensible answer, `400` is arguable too. Pick one and explain it.

The due date is inconsistent:

```json
{
  "borrower": "camille.martin@example.com",
  "due_date": "2026-07-01"
}
```
```http
HTTP/1.1 400 Bad Request
```
```json
{
  "due_date": ["The due date must be later than today."]
}
```

#### Return a book, `POST /api/loans/12/return/`

The request body may be empty. The return date is the current day.

```http
HTTP/1.1 200 OK
```
```json
{
  "id": 12,
  "book": 3,
  "borrower": "camille.martin@example.com",
  "loan_date": "2026-08-03",
  "due_date": "2026-08-17",
  "return_date": "2026-08-10"
}
```

The loan has already been closed:

```http
HTTP/1.1 400 Bad Request
```
```json
{
  "detail": "This loan was already closed on 2026-08-10."
}
```

#### Delete a book, `DELETE /api/books/3/`

```http
HTTP/1.1 204 No Content
```

If the book is currently on loan, the decision is yours: an explicit refusal, cascading
deletion of the loans, archiving rather than deleting, and so on. All of these are
acceptable answers, none of them is acceptable without a justification.

---

## 5. Constraints

- Stay on SQLite, there is no need to set up another database.
- Do not spend more than 2 hours of actual work. If the six endpoints do not fit in that
  time, make choices and tell us which ones. That is a perfectly valid answer.

---

## 6. Deliverable

Send us either a **`.zip` archive** of your project (without the `.venv` directory), or a
**link to a git repository** we can access.

The project must contain, at its root, a **`description.md`** file structured as follows:

```markdown
# Description

## What I implemented
What works, what does not work or was left out, and why (lack of time, deliberate
prioritisation, and so on).

## Technical decisions
The choices you made and the reasoning behind them: type of views, where the business
logic lives, the HTTP status codes you settled on, the behaviour of deletion, how you
handled availability, packages you added.

## Tools used
Documentation, help sites, AI assistants: what helped you, and with what.

## Difficulties encountered
What you got stuck on, for how long, and how you got out of it (or did not). This
section matters a lot to us. Getting stuck is normal, being able to say so and work
around it is a skill.

## Possible improvements
What you would do with one more day.
```

This file is **at least as important as the code**. It does not need to be long, a single
page is plenty. What matters is that it is honest and concrete.

---

## 7. How we assess

In order of importance:

1. **Autonomy.** Were you able to move forward on your own, find information, make
   choices?
2. **Reasoning.** Are your decisions considered and owned, even if we would have done it
   differently?
3. **Communication.** Does the `description.md` let us understand your approach?
4. **Behaviour.** Do the endpoints respond correctly, is the business rule respected?
5. **Code quality.** Readability, naming, organisation, respect for Django and DRF
   conventions.

We are **not** looking for exhaustive error handling or flawless code.

---

## 8. After the test

We will review your submission, then offer you a 30 minute conversation to go through it
together: your choices, what you would do differently, and a few questions about the code.

Good luck.
