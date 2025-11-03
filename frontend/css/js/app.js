document.addEventListener("DOMContentLoaded", () => {
  const memberForm = document.getElementById("member-form");
  const bookForm = document.getElementById("book-form");
  const membersList = document.getElementById("members-list");
  const booksList = document.getElementById("books-list");
  const loanForm = document.getElementById("loan-form");
  const loansList = document.getElementById("loans-list");
  const memberSelect = loanForm.querySelector("select[name='member_id']");
  const bookSelect = loanForm.querySelector("select[name='book_id']");

  // Fetch and display members
  function fetchMembers() {
    fetch("/api/members")
      .then((response) => response.json())
      .then((data) => {
        membersList.innerHTML = "";
        data.forEach((member) => {
          const li = document.createElement("li");
          li.textContent = `${member.name} (${member.email})`;

          const btn = document.createElement("button");
          btn.textContent = "Remove";
          btn.className = "remove-btn";
          btn.style.marginLeft = "8px";
          btn.addEventListener("click", () => {
            if (!confirm(`Remove member "${member.name}"?`)) return;
            fetch(`/api/members/${member.id}`, { method: "DELETE" })
              .then((res) => {
                if (!res.ok)
                  return res.json().then((j) => {
                    throw j;
                  });
                fetchMembers();
              })
              .catch((err) => {
                console.error(err);
                alert(err.error || "Failed to remove member");
              });
          });

          li.appendChild(btn);
          membersList.appendChild(li);
        });
      });
  }

  // Fetch and display books
  function fetchBooks() {
    fetch("/api/books")
      .then((response) => response.json())
      .then((data) => {
        booksList.innerHTML = "";
        data.forEach((book) => {
          const li = document.createElement("li");
          li.textContent = `${book.title} by ${book.author} ${
            book.available === 0 ? "(loaned)" : ""
          }`;

          const btn = document.createElement("button");
          btn.textContent = "Remove";
          btn.className = "remove-btn";
          btn.style.marginLeft = "8px";
          btn.addEventListener("click", () => {
            if (!confirm(`Remove book "${book.title}"?`)) return;
            fetch(`/api/books/${book.id}`, { method: "DELETE" })
              .then((res) => {
                if (!res.ok)
                  return res.json().then((j) => {
                    throw j;
                  });
                fetchBooks();
              })
              .catch((err) => {
                console.error(err);
                alert(err.error || "Failed to remove book");
              });
          });

          li.appendChild(btn);
          booksList.appendChild(li);
        });
      });
  }

  // Add a new member (send JSON)
  memberForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(memberForm);
    const payload = {
      name: formData.get("name"),
      email: formData.get("email"),
    };
    fetch("/api/members", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (!response.ok)
          return response.json().then((j) => {
            throw j;
          });
        return response.json();
      })
      .then(() => {
        fetchMembers();
        memberForm.reset();
      })
      .catch((err) => {
        alert(err.error || "Failed to add member");
      });
  });

  // Add a new book (send JSON)
  bookForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(bookForm);
    const payload = {
      title: formData.get("title"),
      author: formData.get("author"),
    };
    fetch("/api/books", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (!response.ok)
          return response.json().then((j) => {
            throw j;
          });
        return response.json();
      })
      .then(() => {
        fetchBooks();
        bookForm.reset();
      })
      .catch((err) => {
        alert(err.error || "Failed to add book");
      });
  });

  // Update member select options when members list changes
  function updateMemberSelect() {
    fetch("/api/members")
      .then((response) => response.json())
      .then((members) => {
        memberSelect.innerHTML = '<option value="">Select Member</option>';
        members.forEach((member) => {
          const option = document.createElement("option");
          option.value = member.id;
          option.textContent = `${member.name} (${member.email})`;
          memberSelect.appendChild(option);
        });
      });
  }

  // Update book select options when books list changes
  function updateBookSelect() {
    fetch("/api/books")
      .then((response) => response.json())
      .then((books) => {
        bookSelect.innerHTML = '<option value="">Select Book</option>';
        books.forEach((book) => {
          if (book.available) {
            const option = document.createElement("option");
            option.value = book.id;
            option.textContent = `${book.title} by ${book.author}`;
            bookSelect.appendChild(option);
          }
        });
      });
  }

  // Fetch and display current loans
  function fetchLoans() {
    fetch("/api/loans")
      .then((response) => response.json())
      .then((loans) => {
        loansList.innerHTML = "";
        loans.forEach((loan) => {
          const li = document.createElement("li");
          li.className = "loan-item";

          // Add return button next to loan info
          li.innerHTML = `
                        <div class="loan-info">
                            <span>${loan.member_name} borrowed "${
            loan.book_title
          }"</span>
                            <span>${new Date(
                              loan.loan_date
                            ).toLocaleDateString()}</span>
                        </div>
                        <button class="return-btn" data-loan-id="${
                          loan.id
                        }">Return Book</button>
                    `;

          // Add return button handler
          const returnBtn = li.querySelector(".return-btn");
          returnBtn.addEventListener("click", () => {
            if (!confirm("Confirm book return?")) return;

            fetch(`/api/loans/${loan.id}/return`, {
              method: "POST",
            })
              .then((response) => {
                if (!response.ok)
                  return response.json().then((err) => {
                    throw err;
                  });
                fetchLoans(); // Refresh loans list
                fetchBooks(); // Refresh books list
                updateBookSelect(); // Update loan form options
              })
              .catch((err) => {
                alert(err.error || "Failed to return book");
              });
          });

          loansList.appendChild(li);
        });
      });
  }

  // Handle loan form submission
  loanForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(loanForm);
    const payload = {
      member_id: parseInt(formData.get("member_id")),
      book_id: parseInt(formData.get("book_id")),
    };
    fetch("/api/lend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (!response.ok)
          return response.json().then((err) => {
            throw err;
          });
        return response.json();
      })
      .then(() => {
        fetchLoans();
        fetchBooks(); // Refresh books to update availability
        loanForm.reset();
        updateBookSelect();
      })
      .catch((err) => {
        alert(err.error || "Failed to lend book");
      });
  });

  // Initial fetch of members and books
  fetchMembers();
  fetchBooks();

  // Initialize loan form
  updateMemberSelect();
  updateBookSelect();
  fetchLoans();

  // Update selects when lists change
  memberForm.addEventListener("submit", () =>
    setTimeout(updateMemberSelect, 500)
  );
  bookForm.addEventListener("submit", () => setTimeout(updateBookSelect, 500));
});
